Check_MK plugin for Alpine Linux LBU Status
===========================================


About
-----

This check-mk package retrieves the monitor states of non-commited changes with `lbu status` using ssh to connect to the host.


Install
-------

Clone this repository and copy the folders `agent_based` and `rulesets` to the following location on your CheckMK installation:

`/omd/sites/[SITE_NAME]/local/lib/python3/cmk_addons/plugins/lbu_status/`

If the previous version of this plugin is used, remove it by deinstall the mkp package.

Copy the agent to the agent plugin directory on your host you want to monitor.

Setup
-----

When the plugin detects pending changes it switch to a warning or critical status.
This can be edited via rules.
