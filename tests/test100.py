from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.router.config import CommunityList, BGP, OSPF6, AccessList, RouterConfig, AF_INET6, AF_INET, set_rr, ebgp_session, SHARE, IP6Tables, InputFilter, Deny, Allow, Rule, bgp_fullmesh, bgp_peering, ebgp_session, CLIENT_PROVIDER, SHARE


class MyTopology(IPTopo):

    def build(self, *args, **kwargs):

        r1 = self.addRouter("r1" ,lo_addresses=["2042:1::1/64","10.1.0.1/32"])
        r11 = self.addRouter("r11", lo_addresses=["2042:2::1/64","10.2.0.1/32"])
        rh1 = self.addRouter("rh1", lo_addresses=["2042:4::1/64","10.4.0.1/32"])
        r2 = self.addRouter("r2", lo_addresses=["2042:3::1/64","10.3.0.1/32"])
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        # h3 = self.addHost("h3")

        r1.addDaemon(BGP)
        r11.addDaemon(BGP)
        
        r2.addDaemon(BGP, address_families=(
            AF_INET(redistribute=('connected',)),
            AF_INET6(redistribute=( 'connected',))))
        rh1.addDaemon(BGP, address_families=(
            AF_INET(redistribute=('connected',)),
            AF_INET6(redistribute=('connected',))))

        lr1r2 = self.addLink(r1, r2)
        lr1r2[r1].addParams(ip=("2042:12::1/64","10.12.0.1/30"))
        lr1r2[r2].addParams(ip=("2042:12::2/64","10.12.0.2/30"))

        # lr1r11 = self.addLink(r11, r1)

        lh1rh1 = self.addLink(h1, rh1)
        lh1rh1[h1].addParams(ip=("2042:5e::1/64","10.10.0.1/30"))
        lh1rh1[rh1].addParams(ip=("2042:5e::a/64","10.10.0.2/30"))


        lr1rh1 = self.addLink(r1, rh1, igp_metric = 5)
        lr1rh1[r1].addParams(ip=("2042:1a::1/64","10.51.0.1/30"))
        lr1rh1[rh1].addParams(ip=("2042:1a::a/64","10.51.0.2/30"))

        lr11rh1 = self.addLink(r11, rh1 , igp_metric = 10)
        lr11rh1[r11].addParams(ip=("2042:3c::2/64","10.64.0.1/30"))
        lr11rh1[rh1].addParams(ip=("2042:3c::b/64","10.64.0.2/30"))


        lr2h2 = self.addLink(r2, h2)
        lr2h2[r2].addParams(ip=("2042:2b::2/64","10.62.0.1/30"))
        lr2h2[h2].addParams(ip=("2042:2b::b/64","10.62.0.2/30"))


        lr2r11 = self.addLink(r2, r11,)
        lr2r11[r2].addParams(ip=("2042:4d::2/64","10.70.0.1/30"))
        lr2r11[r11].addParams(ip=("2042:4d::b/64","10.70.0.2/30"))

        # lr11h3 = self.addLink(r11, h3)

        self.addAS(1, (r11,r1,rh1))
        bgp_fullmesh(self, [r11,r1,rh1])
        self.addAS(2, (r2,))
        ebgp_session(self, r1, r2)
        ebgp_session(self, r11, r2)

        # loc_pref = CommunityList('loc-pref', '2:80')
        # loc_pref2 = CommunityList('loc-pref2','3:90')
        # al = AccessList(name='all', entries=('any',))


        # r2.get_config(BGP).set_local_pref(80, from_peer=r1, matching=(loc_pref,))
        # r2.get_config(BGP).set_local_pref(120, from_peer=r11, matching=(loc_pref2,))

        # r1.get_config(BGP).set_community(loc_pref, to_peer=r2, matching=(al,))
        # r2.get_config(BGP).set_community(loc_pref2, to_peer=r2, matching=(al,))
        # # r2.get_config(BGP).deny(matching=(loc_pref,))

        super().build(*args, **kwargs)

net = IPNet(topo=MyTopology(),allocate_IPs = False)  # Disable IP auto-allocation
try:
    net.start()
    # print(net['r11'].cmd('python3 scripts/script_comm_R1.py {}'.format(200)))
    # print(net['r1'].cmd('python3 scripts/script_comm_R1.py {}'.format(300)))
    print(net['r2'].cmd('python3 scripts/script_comm_R2.py'))
    print(net['r1'].cmd('python3 scripts/BGP_AS_PREPEND_X1.py'))
    #print(net['r1'].cmd('python3 scripts/BGP_AS_PREPEND_X1.py'))
    
    IPCLI(net)
finally:
    net.stop()