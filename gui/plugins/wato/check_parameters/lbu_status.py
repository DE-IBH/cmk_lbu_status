#!/usr/bin/env python3

# Copyright Philipp Kilian 2018-2022                      kilian@ibh.de

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Tuple,
    Age,
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
    RulespecGroupCheckParametersOperatingSystem,
)


def _parameter_valuespec_lbu_status_levels():
    return Dictionary(
        elements=[
            ("levels",
             Tuple(
                 title=_("Levels"),
                 elements=[
                     Age(
                         title=_("Warning at"),
                         default_value=1800,
                     ),
                     Age(
                         title=_("Critical at"),
                         default_value=3600,
                     ),
                 ],
             )),
        ],
        required_keys=['levels'],  # There is only one value, so its required
    )


rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="lbu_status",
        group=RulespecGroupCheckParametersOperatingSystem,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_lbu_status_levels,
        title=lambda: _("Proxmox VE disk percentage used"),
    ))
