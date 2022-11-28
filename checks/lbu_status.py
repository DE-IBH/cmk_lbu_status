#!/usr/bin/env python3

# cmk_lbu_status - check-mk plugin for Alpine Linux lbu status
#
# Authors:
#   Philipp Kilian <kilian@ibh.de>
#
# Copyright Holder:
#   2018-2022 (C) IBH IT-Service GmbH [http://www.ibh.de/]
#
# License:
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this package; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

# Example output from agent
# changes_since_seconds change_action file
# <<<lbu_status>>>
# 1940 A /etc/added.txt
# 275 U /etc/modified.txt
# 0 D /etc/deleted.txt

from typing import Any, List, Literal, Mapping
from datetime import datetime as dt
from datetime import timedelta as td

from .agent_based_api.v1 import register, Result, Service, State
from .agent_based_api.v1.type_defs import DiscoveryResult, InventoryResult, CheckResult, StringTable


class LBU:
    time: td
    mode: Literal["A", "U", "D"]
    path: str

    def get_time_in_seconds(self) -> int:
        return self.time.days * 86400 + self.time.seconds

    def get_time_string(self) -> str:
        return (dt.now() - self.time).strftime("%Y-%m-%d %H:%M:%S")

    def __init__(self, time: int, mode: Literal["A", "U", "D"], path: str):
        self.time = td(seconds=time)
        self.mode = mode
        self.path = path


def check_lbu_status(params: Mapping[str, Any], section: List[LBU]) -> CheckResult:
    warn, crit = params.get("levels", (1800, 3600))
    max_time = 0
    deleted = False
    state = State.OK

    number_of_changes = len(section)
    if number_of_changes == 0:
        summary = "no pending changes"
    elif number_of_changes == 1:
        max_time = section[0].get_time_in_seconds()
        if section[0].mode == "D":
            summary = str(number_of_changes) + " pending change"
            deleted = True
        else:
            summary = f"{number_of_changes} pending change since {section[0].get_time_string()}"
    else:
        max_time_string = ""
        for lbu_index in range(len(section)):
            seconds = section[lbu_index].get_time_in_seconds()
            if section[lbu_index].mode != "D":
                if max_time < seconds:
                    max_time = seconds
                    max_time_string = section[lbu_index].get_time_string()
            else:
                deleted = True
        if deleted:
            summary = f"{number_of_changes} pending changes"
        else:
            summary = f"{number_of_changes} pending change since {max_time_string}"

    if deleted or crit <= max_time:
        state = State.CRIT
    elif warn <= max_time < crit:
        state = State.WARN

    yield Result(state=state, summary=summary)


def discovery_lbu_status(section: List[LBU]) -> InventoryResult:
    yield Service()


def parse_lbu_status(string_table: StringTable) -> List[LBU]:
    lbu_list = []
    for entry in string_table:
        lbu_list.append(LBU(int(entry[0]), entry[1], entry[2]))
    return lbu_list


register.agent_section(
    name="lbu_status",
    parse_function=parse_lbu_status,
)

register.check_plugin(
    name="lbu_status",
    service_name="LBU Status",
    discovery_function=discovery_lbu_status,
    check_function=check_lbu_status,
    check_ruleset_name="lbu_status",
    check_default_parameters={"levels": (1800, 3600)}
)

