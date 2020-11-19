from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.router.config import CommunityList, BGP, OSPF6, AccessList, RouterConfig, AF_INET6, AF_INET, set_rr, ebgp_session, SHARE, IP6Tables, InputFilter, Deny, Allow, Rule, bgp_fullmesh, bgp_peering, ebgp_session, CLIENT_PROVIDER, SHARE
import time

class MyTopology(IPTopo):

    def build(self, *args, **kwargs):

        r1 = self.addRouter("r1" ,lo_addresses=["2042:1::1/64","10.1.0.1/32"])
        r2 = self.addRouter("r2", lo_addresses=["2042:3::1/64","10.3.0.1/32"])
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        # h3 = self.addHost("h3")

        r1.addDaemon(BGP,debug=("updates",))
        
        
        r2.addDaemon(BGP, address_families=(
            AF_INET(redistribute=('connected',)),
            AF_INET6(redistribute=( 'connected',))),debug=("updates",))
        

        lr1r2 = self.addLink(r1, r2)
        lr1r2[r1].addParams(ip=("2042:12::1/64","10.12.0.1/30"))
        lr1r2[r2].addParams(ip=("2042:12::2/64","10.12.0.2/30"))

        # lr1r11 = self.addLink(r11, r1)

        lh1rh1 = self.addLink(h1, rh1)
        lh1rh1[h1].addParams(ip=("2042:5e::1/64","10.10.0.1/30"))
        lh1rh1[rh1].addParams(ip=("2042:5e::a/64","10.10.0.2/30"))


        lr1rh1 = self.addLink(r1, rh1,igp_metric=10)
        lr1rh1[r1].addParams(ip=("2042:1a::1/64","10.51.0.1/30"))
        lr1rh1[rh1].addParams(ip=("2042:1a::a/64","10.51.0.2/30"))

        lr11rh1 = self.addLink(r11, rh1, igp_metric=15)
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
    general_route_map = "general_route_map"
    
    community_as_prepend_x1 = "1:100"
    community_as_prepend_x1_name = "prepend_x1"
    community_as_prepend_x2 = "2:100"
    community_as_prepend_x2_name = "prepend_x2"

    community_local_pref_200 = "200:200"
    community_local_pref_200_name = "local_pref_200"
    # adding x1 and x2 communities to every packet
    print(net['r2'].cmd('python3 scripts/BGP_SET_ANY_COMM_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x1,general_route_map,10)))
    print(net['r2'].cmd('python3 scripts/BGP_SET_ANY_COMM_RMNAME_SEQ.py {} {} {}'.format(community_local_pref_200,general_route_map,20)))
    print(net['r2'].cmd('python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map,100)))
    print(net['r2'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format("2042:12::1",general_route_map,"out")))


    print(net['r1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x1,community_as_prepend_x1_name)))
    print(net['r1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_local_pref_200,community_local_pref_200_name)))
    print(net['r1'].cmd('python3 scripts/BGP_COMML_LPREF_RMNAME_SEQ.py {} {} {} {}'.format(community_local_pref_200_name,200,general_route_map,10)))
    print(net['r1'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x1_name,general_route_map,20)))
    print(net['r1'].cmd('python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map,100)))
    print(net['r1'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format("2042:12::2",general_route_map,"in")))
 


    # print(net['r1'].cmd('python3 scripts/BGP_LPREF.py  {}'.format(300)))
    # print(net['r11'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format("2042:12::2", "TEST", "in")))
    # print(net['r11'].cmd('python3 scripts/BGP_LPREF.py  {}'.format(200)))
    # print(net['r2'].cmd('python3 scripts/BGP_LPREF.py  {}'.format(150)))
    IPCLI(net)
    
finally:
    net.stop()