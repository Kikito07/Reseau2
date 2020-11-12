#!/usr/bin/env python3

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, OSPF6, RouterConfig, AF_INET6, AF_INET, set_rr, ebgp_session, SHARE, IP6Tables, InputFilter, Deny, Allow, Rule, bgp_fullmesh, bgp_peering, ebgp_session


class SimpleBGPTopo(IPTopo):

    def build(self, *args, **kwargs):

        """
        h1 +------+ R1 +----|---150------+ R2 +-----+ h2
                     -      |            -
                       100  |         -
                          - |      -
                            | R3
                AS1         |        AS2
        """

        r1 = self.addRouter("r1", lo_addresses=["2042:1::1/64","10.1.0.1/32"])
        r2 = self.addRouter("r2", lo_addresses=["2042:2::1/64","10.2.0.1/32"])
        r3 = self.addRouter("r3", lo_addresses=["2042:3::1/64","10.3.0.1/32"])
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")

        r1.addDaemon(BGP, address_families=(
            AF_INET(redistribute=('connected',)),
            AF_INET6(redistribute=('connected',))))
        
        r2.addDaemon(BGP, address_families=(
            AF_INET(redistribute=('connected',)),
            AF_INET6(redistribute=('connected',))))

        r3.addDaemon(BGP, address_families=(
            AF_INET(redistribute=('connected',)),
            AF_INET6(redistribute=('connected',))))

        lr1r2 = self.addLink(r1, r2)
        lr1r2[r1].addParams(ip=("2042:12::1/64","10.12.0.1/30"))
        lr1r2[r2].addParams(ip=("2042:12::2/64","10.12.0.2/30"))

        lr1r3 = self.addLink(r1, r3)
        lr1r3[r1].addParams(ip=("2042:13::1/64","10.13.0.1/30"))
        lr1r3[r3].addParams(ip=("2042:13::2/64","10.13.0.2/30"))

        lr2r3 = self.addLink(r2, r3)
        lr2r3[r2].addParams(ip=("2042:23::1/64","10.23.0.1/30"))
        lr2r3[r3].addParams(ip=("2042:23::2/64","10.23.0.2/30"))

        lr1h1 = self.addLink(r1, h1)
        lr1h1[r1].addParams(ip=("2042:1a::1/64","10.51.0.1/30"))
        lr1h1[h1].addParams(ip=("2042:1a::a/64","10.51.0.2/30"))

        lr2h2 = self.addLink(r2, h2)
        lr2h2[r2].addParams(ip=("2042:2b::2/64","10.62.0.1/30"))
        lr2h2[h2].addParams(ip=("2042:2b::b/64","10.62.0.2/30"))

        r1.get_config(BGP).set_local_pref(150, from_peer=r2)
        r2.get_config(BGP).set_local_pref(150, from_peer=r1)
        r1.get_config(BGP).set_local_pref(100, from_peer=r3)
        r3.get_config(BGP).set_local_pref(100, from_peer=r1)

        self.addAS(1, (r1,))
        self.addAS(2, (r2, r3))
        ebgp_session(self, r1, r2)
        ebgp_session(self, r1, r3)


        # loc_pref = CommunityList('loc-pref', '2:80')
        # al = AccessList(name='all', entries=('any',))
        # r1.get_config(BGP).set_community(loc_pref, to_peer=r2, matching=(al,))
        # r2.get_config(BGP).deny(matching=(loc_pref,))

        super().build(*args, **kwargs)

if __name__ == '__main__':
    net = IPNet(topo=SimpleBGPTopo())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()