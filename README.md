Check_MK plugin for Alpine Linux LBU Status
===========================================


About
-----

This Check_MK package retrieves the monitor states of non-commited changes of Alpine Linux's *Local Backup* (`lbu status`). The package contains an agent plugin which is required to be deployed to the target hosts.


Install
-------

Download the Check_MK package from [GitHub Releases](https://github.com/DE-IBH/cmk_lbu_status/releases) and install it using Check_MK's 
[package manager](https://mathias-kettner.de/cms_mkps.html#Installation%20eines%20MKPs-1).

```console
OMD[mysite]:~$ mkp install lbu_status-x.y.mkp
```


Setup
-----

When the plugin detects pending changes it switch to a warning or critical status depending of the threshold check parameters. The parameters `threshold_warning` and `threshold_critical` can be configured using WATO. Deletions always trigger a critical status.
