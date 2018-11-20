#!/usr/bin/env python

from mininet.topo import Topo
from mininet.node import Host

from bmv2 import ONOSBmv2Switch

PIPECONF_ID = 'org.onosproject.pipelines.fabric'

class SR_P4TOPO(Topo):

    spineswitch = []
    leafswitch = []
    host = []

    def __init__(self):

        # initialize topology
        Topo.__init__(self)

        for i in range(1, 3):
            # add spine switches
            self.spineswitch.append(self.addSwitch("spine"+str(i), cls=ONOSBmv2Switch, pipeconf=PIPECONF_ID))

            # add leaf switches
            self.leafswitch.append(self.addSwitch("leaf"+str(i), cls=ONOSBmv2Switch, pipeconf=PIPECONF_ID))

        # add hosts
        self.host.append(self.addHost("3001", mac="00:00:00:00:00:01", ip="10.6.1.1/24", gateway="10.6.1.254"))
        self.host.append(self.addHost("3002", mac="00:00:00:00:00:02", ip="10.6.1.2/24", gateway="10.6.1.254"))
        self.host.append(self.addHost("3003", mac="00:00:00:00:00:03", ip="10.6.2.1/24", gateway="10.6.2.254"))
        self.host.append(self.addHost("3004", mac="00:00:00:00:00:04", ip="10.6.2.2/24", gateway="10.6.2.254"))

        # add links
        for i in range(2):
            self.addLink(self.spineswitch[i], self.leafswitch[0])
            self.addLink(self.spineswitch[i], self.leafswitch[1])

        for i in range(2):
            self.addLink(self.leafswitch[i], self.host[i*2])
            self.addLink(self.leafswitch[i], self.host[i*2+1])

topos = {'sr-p4': (lambda: SR_P4TOPO())}

if __name__ == "__main__":
    from onosnet import run
    run(SR_P4TOPO())
