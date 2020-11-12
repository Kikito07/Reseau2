from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, OSPF6, OSPF, RouterConfig, AF_INET6, AF_INET, set_rr, ebgp_session, SHARE, IP6Tables, InputFilter, Deny, Allow, Rule, bgp_fullmesh, bgp_peering, ebgp_session


class SimpleBGPTopo(IPTopo):

    arnaud = self.addRouteur("arnaud", config = RouterConfig)
    lahousse = self.addRouteur("lahousse", config = RouterConfig)

    nikita = self.addRouteur("nikita", config = RouterConfig)
    russe = self.addRouteur("russe", config = RouterConfig)
 
 #=============================================================
    arnaud.addDaemon(OSPF6)
    lahousse.addDaemon(OSPF6)

    arnaud.addDaemon(OSPF)
    lahousse.addDaemon(OSPF)
    
    arnaud.addDaemon(("updates",)))
    lahousse.addDaemon(("updates",)))


    nikita.addDaemon(OSPF)
    russe..addDaemon(OSPF6)

    nikita.addDaemon(OSPF)
    russe..addDaemon(OSPF6)

    nikita.addDaemon(("updates",)))
    russe..addDaemon(("updates",)))

#===============================================================

    l_arnaud_lahousse = self.addLink(arnaud, lahousse)
    l_nikita_russe = self.addLink(nikita,russe)

    l_arnaud_nikita = self.addLink(arnaud, nikita)
    l_lahousse_russe = self.addLink(lahousse, russe)
        