# Segment Routing with ONOS

## Introduction

This respository provides topology and configuration files of Segment Routing on ONOS, with OvS, P4 and hybrid switches.

## Usage

Make sure you have [ONOS](https://github.com/opennetworkinglab/onos.git) installed and able to be executed. To be mentioned, I only ran with ONOS version 1.15.

The test was ran with [STC deployment](https://wiki.onosproject.org/display/ONOS/Cells+and+ONOS+test+scripts).

Copy cell files.
```
$ cp test/cells/teston $ONOS_ROOT/tools/test/cells/
```

Load cell environment variables.
```
$ cell teston
```

Deploy with STC.
```
$ stc setup
```

Note: I ran with ONOS version 1.15 and there were errors with `onos-check-nodes` steps, which resulted from that the output of `sort` pipe from `echo` had unknown prefixed characters. As you can see in `$ONOS_ROOT/tools/test/bin/onos-check-nodes`. Although, it should be fine even these errors occurs. It seemed like there was no such problem with ONOS version 1.14 but I did not verify.

Load the configuration file.
```
$ onos-netcfg $OC1 configOVS.json
```

Run the Mininet script.
```
$ sudo -E python topoOVS.py
```

You could execute `pingall` at Mininet shell and hosts should be able to reach each others.

In `test/topos` there is a topology file provided which should also be able to be deployed with STC. But I could not successfully execute `stc net-setup`, even with the defualt topology. Still, I only ran with ONOS version 1.15.
