#!/usr/bin/env python3

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, OSPF6, RouterConfig, AF_INET6, set_rr, ebgp_session, SHARE, IP6Tables, InputFilter, Deny, Allow, Rule



class SimpleBGPTopo(IPTopo):
    """
    Please read me before digging in the code of this script.

    This simple network topology tries to connect two hosts separated
    by multiple routers and ASes.

    Running this network should be straightforward:
     i./ The script must be run as root since mininet will create routers inside your own machine
         $ chmod +x main.py
         $ sudo ./main.py
    
    ii./ The network should be started. The "mininet" CLI should appear on screen
    '''
    mininet>
    '''

    To access to one of the network, execute this command "xterm <your node name>". A new
    xterm terminal will be spawned. This new terminal will run bash. This means that you
    can execute any linux command. Be careful as the terminal is run as root!!

    '''
    mininet> xterm as1_rr1
    '''

    To access to the configuration of FRRouting, you have to use telnet to connect to
    FRRouting daemons.
    A different port is used to access to every routing daemon. This small table shows
    the port associated to its default daemon:

    PORT     STATE SERVICE
    2601/tcp open  zebra   --> controls the RIB of each daemon
    2605/tcp open  bgpd    --> show information related to the configuration of BGP
    2606/tcp open  ospf6d  --> same but for OSPFv3 (OSPF for IPv6)

    For example, if you want to look for all prefixes contained in the RIB, you must execute
    this command :
    <in the xterm of your node>$ telnet localhost 2601

    A new cli interface will be shown:

    '''
    Trying ::1...
    Connected to localhost
    Escape character is '^]'.

    Hello, this is FRRouting (version v7.4).
    Copyright 1996-2005 Kunihiro Ishiguro, et al.

    User Access Verification

    Password:
    '''

    At this time, you will be prompted for a password. In ipmininet the default password is "zebra".
    Simply type it and the FRRouting CLI will be shown:

    '''
    as1_rr1>
    '''

    Type "show ipv6 route" to show all the routes contained in the RIB. You can find an example of output below
    ''''
    as1_rr1> show ipv6 route
    Codes: K - kernel route, C - connected, S - static, R - RIPng,
           O - OSPFv3, I - IS-IS, B - BGP, N - NHRP, T - Table,
           v - VNC, V - VNC-Direct, A - Babel, D - SHARP, F - PBR,
           f - OpenFabric,
           > - selected route, * - FIB route, q - queued route, r - rejected route

    B>* c1a4:4ad:c0ff:ee::/64 [20/0] via fe80::f802:bbff:fe6d:4da0, as1_rr1-eth2, weight 1, 00:50:34
    O>* cafe:babe:dead:beaf::/64 [110/2] via fe80::2c5c:4ff:fe4a:2b73, as1_rr1-eth1, weight 1, 00:50:30
    O   fc00:0:3::/48 [110/1] is directly connected, as1_rr1-eth0, weight 1, 00:50:35
    C>* fc00:0:3::/48 is directly connected, as1_rr1-eth0, 00:50:38
    O   fc00:0:4::/48 [110/1] is directly connected, as1_rr1-eth1, weight 1, 00:50:35
    C>* fc00:0:4::/48 is directly connected, as1_rr1-eth1, 00:50:38
    B   fc00:0:5::/48 [20/0] via fe80::f802:bbff:fe6d:4da0, as1_rr1-eth2, weight 1, 00:50:34
    O   fc00:0:5::/48 [110/1] is directly connected, as1_rr1-eth2, weight 1, 00:50:38
    C>* fc00:0:5::/48 is directly connected, as1_rr1-eth2, 00:50:38
    O>* fc00:0:6::/48 [110/2] via fe80::c07a:14ff:feaf:83d3, as1_rr1-eth0, weight 1,  00:50:30
    O>* fc00:0:7::/48 [110/2] via fe80::c07a:14ff:feaf:83d3, as1_rr1-eth0, weight 1, 00:50:30
    B   fc00:0:7::/48 [200/0] via fc00:0:3::1, as1_rr1-eth0, weight 1, 00:50:34
    O>* fc00:0:8::/48 [110/2] via fe80::2c5c:4ff:fe4a:2b73, as1_rr1-eth1, weight 1, 00:50:30
    O   fc00:0:9::/48 [110/1] is directly connected, lo, weight 1, 00:50:38
    C>* fc00:0:9::/48 is directly connected, lo, 00:50:39
    O>* fc00:0:a::/48 [110/2] via fe80::c07a:14ff:feaf:83d3, as1_rr1-eth0, weight 1, 00:50:30
    O>* fc00:0:b::/48 [110/3] via fe80::2c5c:4ff:fe4a:2b73, as1_rr1-eth1, weight 1, 00:50:25
      *                       via fe80::c07a:14ff:feaf:83d3, as1_rr1-eth0, weight 1, 00:50:25
    O>* fc00:0:c::/48 [110/2] via fe80::2c5c:4ff:fe4a:2b73, as1_rr1-eth1, weight 1, 00:50:30
    B>* fc00:0:d::/48 [20/0] via fe80::f802:bbff:fe6d:4da0, as1_rr1-eth2, weight 1, 00:50:34
    B>* fc00:0:e::/48 [200/0] via fc00:0:3::1, as1_rr1-eth0, weight 1, 00:50:34
    C * fe80::/64 is directly connected, as1_rr1-eth0, 00:50:38
    C * fe80::/64 is directly connected, as1_rr1-eth2, 00:50:38
    C>* fe80::/64 is directly connected, as1_rr1-eth1, 00:50:38
    '''

    Press CTRL + D to exit the session. And again to exit the xterm session.

    You can find more information on how to use the CLI of FRRouting daemons in the FRRouting DOCS:
    http://docs.frrouting.org/en/latest/

    Remember that xterm launches a root bash. You can run any executable (in ROOT!).
    If wireshark is installed on your computer, you can execute it to capture packets
    reaching interfaces of your mininet node.

    The same applies if you want to check the Linux FIB (ip addr) or the addresses attached to the node
    interfaces (ip route)

    Finally, you can find other details on how to build an ipmininet script here:
    https://ipmininet.readthedocs.io/en/latest/
    """

    # 1. Can you picture the topology described in this python script ?
    #    Draw this topology by hand before running it in ipmininet.
    # 2. This small network is faulty. Can you find the problem ?
    # 3. Propose a fix to make this network operational again
    # 4. How can you do to check the LSDB of OSPF ?
    # 5. Again use it to show details abol_PAR1_PAR2[PAR1].addParams(ip=(europe_ipv6 + "00:1201::/64"))ut the BGP sessions.
    # 6. Add a new AS (AS3) on top of this topology which will contain 4 routers, each running
    #    OSPFv3 and BGP. Add also a new host as3_h3 in a new lan taco:d0d0:i5:dead::/64 in one of the 4 routers.
    #    h1, h2 and h3 must reach each other. The iBGP sessions, this time, must be in
    #    full mesh configuration. AS3 will have only one eBGP peering with AS1 on the as1_s1 router.

    def build(self, *args, **kwargs):

        monde_ipv6 = "1627:6100:0000"
        europe_ipv6 = monde_ipv6 + ":0"
        NA_ipv6 = monde_ipv6 + ":1"
        asia_ipv6 = monde_ipv6 + ":2"

        # first step, adding routers
       

        PAR1 = self.addRouter("PAR1", lo_addresses=[europe_ipv6 + "200::/64"])
        PAR2 = self.addRouter("PAR2", lo_addresses=[europe_ipv6 + "300::/64"])    
        
        # firewall for router
        
        
        # adding OSPF6 as IGP
       
        PAR2.addDaemon(OSPF6)
        #PAR2.addDaemon(IP6Tables, rules=ip_rules_PAR2)

        H1 = self.addHost("H1")
        H2 = self.addHost("H2")
       
        l_PAR1_PAR2 = self.addLink(PAR1, PAR2)
        l_PAR1_PAR2[PAR1].addParams(ip=(europe_ipv6 + "201::/64"))
        l_PAR1_PAR2[PAR2].addParams(ip=(europe_ipv6 + "301::/64"))

        l_PAR1_H1 = self.addLink(PAR1, H1)
        l_PAR1_H1[PAR1].addParams(ip=(europe_ipv6 + "202::/64"))
        l_PAR1_H1[H1].addParams(ip=(europe_ipv6 + "001::/64"))

        l_PAR2_H2 = self.addLink(PAR2, H2)
        l_PAR2_H2[PAR2].addParams(ip=(europe_ipv6 + "302::/64"))
        l_PAR2_H2[H2].addParams(ip=(europe_ipv6 + "002::/64"))

        


        super().build(*args, **kwargs)


# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=SimpleBGPTopo(), allocate_IPs = False)
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
