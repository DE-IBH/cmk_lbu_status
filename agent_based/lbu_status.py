#!/usr/bin/env python3

# cmk_lbu_status - check-mk plugin for Alpine Linux lbu status
#
# Authors:
#   Philipp Kilian <kilian@ibh.de>
#
# Copyright Holder:
#   2018-2025 (C) IBH IT-Service GmbH [http://www.ibh.de/]
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

from cmk.agent_based.v2 import AgentSection, CheckPlugin, Metric, Result, Service, State, StringTable


class LBU:
    time: td
    mode: Literal["A", "U", "D"]
    path: str

    def __init__(self, time: int, mode: Literal["A", "U", "D"], path: str):
        self.time = td(seconds=time)
        self.mode = mode
        self.path = path

    def __str__(self):
        return f"{self.mode} {self.get_time_in_seconds} {self.path}"

    @property
    def get_time_in_seconds(self) -> int:
        return self.time.days * 86400 + self.time.seconds

    @property
    def get_time_string(self) -> str:
        return (dt.now() - self.time).strftime("%Y-%m-%d %H:%M:%S")


def check_lbu_status(params: Mapping[str, Any], section: List[LBU]):
    warn = params["warning_seconds"]
    crit = params["critical_seconds"]
    max_time = 0
    deleted = False
    state = State.OK
    details = None

    number_of_changes = len(section)
    if number_of_changes == 0:
        summary = "no pending changes"
    elif number_of_changes == 1:
        max_time = section[0].get_time_in_seconds
        if section[0].mode == "D":
            summary = str(number_of_changes) + " pending change"
            deleted = True
        else:
            summary = f"{number_of_changes} pending change since {section[0].get_time_string}"
        details = section[0].__str__()
    else:
        max_time_string = ""
        for lbu in section:
            seconds = lbu.get_time_in_seconds
            if lbu.mode != "D":
                if max_time < seconds:
                    max_time = seconds
                    max_time_string = lbu.get_time_string
            else:
                deleted = True
            if details is None:
                details = f"{lbu.__str__()}"
            else:
                details += f"\n{lbu.__str__()}"
        if deleted:
            summary = f"{number_of_changes} pending changes"
        else:
            summary = f"{number_of_changes} pending change since {max_time_string}"

    if deleted or crit <= max_time:
        state = params["critical_state"]
    elif warn <= max_time < crit:
        state = params["warning_state"]

    yield Result(state=state, summary=summary, details=details)


def discovery_lbu_status(section: List[LBU]):
    yield Service()


def parse_lbu_status(string_table: StringTable) -> List[LBU]:
    lbu_list = []
    for entry in string_table:
        lbu_list.append(LBU(int(entry[0]), entry[1], entry[2]))
    return lbu_list


agent_section_lbu_status = AgentSection(
    name="lbu_status",
    parse_function=parse_lbu_status,
)


check_plugin_lbu_status = CheckPlugin(
    name="lbu_status",
    sections=["lbu_status"],
    service_name="LBU Status",
    discovery_function=discovery_lbu_status,
    check_function=check_lbu_status,
    check_ruleset_name="lbu_status_rules",
    check_default_parameters={
        "critical_seconds": 3600,
        "critical_state": State.CRIT,
        "warning_seconds": 1800,
        "warning_state": State.WARN
    }
)

