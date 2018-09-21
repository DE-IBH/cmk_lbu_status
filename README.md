check-mk plugin for Alpine Linux LBU Status
===========================================


About
-----

This check-mk package retrieves the monitor states of non-commited changes with `lbu status` using ssh to connect to the host.


Install
-------

Download the provided check-mk package `lbu_status-x.y.mkp` and install it using *check-mk*'s 
[package manager](https://mathias-kettner.de/cms_mkps.html#Installation%20eines%20MKPs-1).


```console
# mkp install [..]/lbu_status-x.y.mkp
```

Setup
-----

This package checks the time of changes of  `lbu status` output for added and modified files. It sends a warning or 
critical message based on the parameters `threshold_warning` and `threshold_critical`.

For deleted files it gives always a critical message
