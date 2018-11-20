# 2-by-2 leaf-spine topology
import os
import sys

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController, Host, OVSSwitch
from mininet.link import TCLink
from mininet.log import setLogLevel, info, warn

class MyTopo(Topo):

    spineswitch = []
    leafswitch = []
    host = []

    def __init__(self):

        # initialize topology
        Topo.__init__(self)

        for i in range(1, 3):
            # add spine switches
            self.spineswitch.append(self.addSwitch("100"+str(i), dpid="000000000000019"+str(i)))

            # add leaf switches
            self.leafswitch.append(self.addSwitch("200"+str(i), dpid="000000000000010"+str(i)))

        # add hosts
        # for i in range(1, 5):
        #     self.host.append(self.addHost("300"+str(i), mac="00:00:00:00:00:0"+str(i)))
        self.host.append(self.addHost("3001", cls=IpHost, mac="00:00:00:00:00:01", ip="10.6.1.1/24", gateway="10.6.1.254"))
        self.host.append(self.addHost("3002", cls=IpHost, mac="00:00:00:00:00:02", ip="10.6.1.2/24", gateway="10.6.1.254"))
        self.host.append(self.addHost("3003", cls=IpHost, mac="00:00:00:00:00:03", ip="10.6.2.1/24", gateway="10.6.2.254"))
        self.host.append(self.addHost("3004", cls=IpHost, mac="00:00:00:00:00:04", ip="10.6.2.2/24", gateway="10.6.2.254"))

        # add links
        for i in range(2):
            self.addLink(self.spineswitch[i], self.leafswitch[0])
            self.addLink(self.spineswitch[i], self.leafswitch[1])

        for i in range(2):
            self.addLink(self.leafswitch[i], self.host[i*2])
            self.addLink(self.leafswitch[i], self.host[i*2+1])

class IpHost(Host):
    def __init__(self, name, gateway, *args, **kwargs):
        super(IpHost, self).__init__(name,*args,**kwargs)
        self.gateway = gateway

    def config(self, **kwargs):
        Host.config(self,**kwargs)
        mtu = "ifconfig " + self.name + "-eth0 mtu 1490"
        self.cmd(mtu)
        self.cmd('ip route add default via %s' % self.gateway)

topos = {'mytopo': (lambda: MyTopo())}

if 'OC1' not in os.environ:
    raise Exception( "Environment var $OC1 not set" )
OC1 = os.environ['OC1']

if __name__ == "__main__":
    setLogLevel('info')

    if len(sys.argv) == 1:
        controllerIp = OC1
    elif len(sys.argv) == 2:
        controllerIp = sys.argv[1]
    else:
        warn("Usage: %s [controller IP]\n" % sys.argv[0])
        sys.exit(1)

    info("Controller IP %s is used.\n" % controllerIp)

    topo = MyTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None)
    net.addController('c0', switch=OVSSwitch, controller=RemoteController, ip=controllerIp)

    net.start()
    CLI(net)
    net.stop()
