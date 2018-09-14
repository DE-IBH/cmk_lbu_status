#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Put this file into the PLUGINSDIR [$MK_LIBDIR/plugins] of the agent system

import subprocess as sp
from datetime import datetime as dt

lbu_status_result_obj = sp.Popen("lbu status", shell=True)
if lbu_status_result_obj.returncode != 0:
    exit()

current_time = dt.now()

print "<<<lbu_status>>>"

for result in lbu_status_result_obj.stdout:
    changemode = result.replace("\n", "").split(" ")[0]
    if len(result.split(" ")) > 2:
        splitted_result = result.replace("\n", "").split(" ")
        filepath = "/" + splitted_result[1]
        for result_part in splitted_result[2:]:
             filepath += " " + result_part
    else:
        filepath = "/" + result.replace("\n", "").split(" ")[1]
    if changemode == "A" or changemode == "U":
        changetime = dt.fromtimestamp(os.path.getmtime(filepath))
        seconds = (current_time - changetime).seconds
        print seconds, changemode, filepath
    else:
        print 0, changemode, filepath
