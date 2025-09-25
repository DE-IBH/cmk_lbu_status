#!/usr/bin/env python3

from cmk.rulesets.v1 import Label, Title
from cmk.rulesets.v1.form_specs import BooleanChoice, DefaultValue, DictElement, Dictionary, Integer, ServiceState
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form_lbu_status():
    return Dictionary(
        elements = {
            "warning_seconds": DictElement(
                parameter_form = Integer(
                    title = Title("Time until warning State"),
                    unit_symbol = "seconds",
                    prefill = DefaultValue(value=1800)
                )
            ),
            "critical_seconds": DictElement(
                parameter_form = Integer(
                    title = Title("Time until critical State"),
                    unit_symbol = "seconds",
                    prefill = DefaultValue(value=3600)
                )
            ),
            "warning_state": DictElement(
                parameter_form = ServiceState(
                    title = Title("Status when warning"),
                    prefill = DefaultValue(value=ServiceState.CRIT)
                )
            ),
            "critical_state": DictElement(
                parameter_form = ServiceState(
                    title = Title("Status when critical"),
                    prefill = DefaultValue(value=ServiceState.CRIT)
                )
            )
        }
    )


rule_spec_lbu_status = CheckParameters(
    name = "lbu_status_rules",
    title = Title("LBU Status"),
    topic = Topic.OPERATING_SYSTEM,
    parameter_form = _parameter_form_lbu_status,
    condition = HostAndItemCondition(item_title = Title("LBU Status"))
)
