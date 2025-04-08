# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import concurrent.futures
import contextlib
import copy
from functools import partial
import logging
import os
import requests
import time

import oslo_config
from oslo_policy import _checks
import oslo_log

from oslo_policy_opa import opts

LOG = logging.getLogger(__name__)


def normalize_name(name: str) -> str:
    return name.translate(str.maketrans({":": "/", "-": "_"}))


class OPACheck(_checks.Check):
    """Oslo.policy ``opa:`` check

    Invoke OPA for the authorization policy evaluation. In case of errors
    fallback to the default rule definition.
    """

    opts_registered = False

    def __call__(self, target, creds, enforcer, current_rule=None):
        if not self.opts_registered:
            opts._register(enforcer.conf)
            self.opts_registered = True

        timeout = enforcer.conf.oslo_policy.remote_timeout

        url = "/".join(
            [
                enforcer.conf.oslo_policy.opa_url,
                "v1",
                "data",
                normalize_name(self.match),
                "allow",
            ]
        )
        json = self._construct_payload(creds, current_rule, enforcer, target)
        try:
            start = time.time()
            with contextlib.closing(
                requests.post(url, json=json, timeout=timeout)
            ) as r:
                end = time.time()
                if r.status_code == 200:
                    result = r.json().get("result")
                    if isinstance(result, bool):
                        return result
                    else:
                        return False
                else:
                    LOG.error(
                        "Exception during checking OPA. Status_code = %s",
                        r.status_code,
                    )
        except Exception as ex:
            LOG.error(
                f"Exception during checking OPA {ex}. Fallback to the DocumentedRuleDefault"
            )
        # When any exception has happened during the communication or OPA
        # result processing we want to fallback to the default rule
        default_rule = enforcer.registered_rules.get(current_rule)
        if default_rule:
            return _checks._check(
                rule=default_rule._check,
                target=target,
                creds=creds,
                enforcer=enforcer,
                current_rule=current_rule,
            )
        return False

    @staticmethod
    def _construct_payload(creds, current_rule, enforcer, target):
        # Convert instances of object() in target temporarily to
        # empty dict to avoid circular reference detection
        # errors in jsonutils.dumps().
        temp_target = copy.deepcopy(target)
        for key in target.keys():
            element = target.get(key)
            if type(element) is object or not (
                isinstance(element, (str, int, float, bool, list, tuple, dict))
                or element is None
            ):
                temp_target[key] = {}
        json = {"input": {"target": temp_target, "credentials": creds}}
        return json


def query_filter(json: dict, url: str, timeout: int):
    try:
        with contextlib.closing(requests.post(url, json=json, timeout=1)) as r:
            if r.status_code == 200:
                return r.json().get("result")
            else:
                LOG.error(
                    "Exception during checking OPA. Status_code = %s",
                    r.status_code,
                )
    except Exception as ex:
        LOG.error(f"Exception during checking OPA {ex}.")


class OPAFilter(OPACheck):
    """Oslo.policy ``opa_filter:`` check

    Invoke OPA for the authorization policy evaluation. It is expected that the
    result is a dict with `allowed: BOOL` and `filtered: DICT_OF_FILTERED_ATTRIBUTES`.
    """

    opts_registered = False

    def __call__(
        self, targets: list[dict], creds, enforcer, current_rule=None
    ):
        if not self.opts_registered:
            opts._register(enforcer.conf)
            self.opts_registered = True

        timeout = enforcer.conf.oslo_policy.remote_timeout

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            url = "/".join(
                [
                    enforcer.conf.oslo_policy.opa_url,
                    "v1",
                    "data",
                    normalize_name(self.match),
                ]
            )
            results = executor.map(
                partial(query_filter, url=url, timeout=timeout),
                [
                    self._construct_payload(
                        creds, current_rule, enforcer, target
                    )
                    for target in targets
                ],
            )
            executor.shutdown()

            for result in results:
                if result.get("allow", False):
                    filtered = result.get("filtered", {})
                    if filtered:
                        yield filtered

    @staticmethod
    def _construct_payload(creds, current_rule, enforcer, target):
        json = {"input": {"target": target, "credentials": creds}}
        return json
