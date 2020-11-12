from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.router.config import BorderRouterConfig, BGP, ebgp_session, AccessList, CommunityList


class SimpleBGPTopo(IPTopo):
    """This topology builds a 3-AS network exchanging BGP reachability
    information"""
    def build(self, *args, **kwargs):
        """
           +----------+                                   +--------+
                      |                                   |
         AS1          |                  AS2              |        AS3
                      |                                   |
                      |                                   |
    +-------+   eBGP  |  +-------+     iBGP    +-------+  |  eBGP   +-------+
    | as1r1 +------------+ as2r1 +-------------+ as2r2 +------------+ as3r1 |
    +-------+         |  +-------+             +-------+  |         +-------+
                      |                                   |
                      |                                   |
                      |                                   |
         +------------+                                   +--------+
        """
        # Add all routers
        as1r1 = self.bgp('as1r1')
        as2r1 = self.bgp('as2r1')
        as2r2 = self.bgp('as2r2')
        as3r1 = self.bgp('as3r1')
        self.addLinks((as1r1, as2r1), (as2r1, as2r2), (as3r1, as2r2))
        # Set AS-ownerships
        self.addAS(1, (as1r1,))
        self.addiBGPFullMesh(2, (as2r1, as2r2))
        self.addAS(3, (as3r1,))
        # Add eBGP peering
        ebgp_session(self, as1r1, as2r1)
        ebgp_session(self, as3r1, as2r2)

        all_al = AccessList('all', ('any',))
        
        
#===================================================================================================

        loc_pref = CommunityList('loc-pref', '2:80')

        as2r1.get_config(BGP).set_local_pref(80, from_peer=as1r1, matching=(loc_pref,))

        as1r1.get_config(BGP).set_community('2:80', to_peer=as2r1, matching=(all_al,))

        as3r1.get_config(BGP).set_med(50, to_peer=as2r2, matching=(all_al,))

#===================================================================================================


        # Add test hosts
        for r in self.routers():
            self.addLink(r, self.addHost('h%s' % r))
        super().build(*args, **kwargs)

    def bgp(self, name):
        r = self.addRouter(name, config=BorderRouterConfig)
        return r

if __name__ == '__main__':
    net = IPNet(topo=SimpleBGPTopo())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()

