#!/usr/bin/env python3

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, OSPF6, OSPF, RouterConfig, AF_INET6, AF_INET, set_rr, ebgp_session, SHARE, IP6Tables, InputFilter, Deny, Allow, Rule, bgp_fullmesh, bgp_peering, ebgp_session
import hashlib


class SimpleBGPTopo(IPTopo):
    
    def build(self, *args, **kwargs):


        r1 = self.addRouter("r1",config=RouterConfig)
        r2 = self.addRouter("r2",config=RouterConfig)

        r1.addDaemon(OSPF6)
        r2.addDaemon(OSPF6)
        r1.addDaemon(OSPF)
        r2.addDaemon(OSPF)
        self.addLink(r1,r2,password = "r1-eth0")
        super().build(*args, **kwargs)

# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=SimpleBGPTopo())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
