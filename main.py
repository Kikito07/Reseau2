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
        
        monde_ipv6 = "1627:6000:0000"
        europe_ipv6 = monde_ipv6 + ":0"
        NA_ipv6 = monde_ipv6 + ":1"
        asia_ipv6 = monde_ipv6 + ":2"
        peer_ipv6 = "dead:beaf:0000::"



        MRS_ipv4 = "162.76.0."
        PAR_ipv4 = "162.76.1."
        SIN_ipv4 = "162.76.2."
        SYD_ipv4 = "162.76.3."
        LAX_ipv4 = "162.76.4."
        SJO_ipv4 = "162.76.5."
        ASH_ipv4 = "162.76.6."

        VDF_ipv4 = "174.50.0"
        EQX_ipv4 = "174.50.1"
        NTT_ipv4 = "174.50.2"

        lan_vodafone_ipv4 = "174.50.0."
        lan_vodafone_ipv6 = "dead:beaf:0000::"
        lan_equinix_ipv4 = "174.50.1."
        lan_equinix_ipv6 = "dead:beaf:0001::"
        lan_ntt_ipv4 = "174.50.2"
        lan_ntt_ipv6 = "dead:beaf:0002::"



        family = AF_INET6()



        # first step, adding routers
        #=========================================================
       
        # routers of MRS
        MRS1 = self.addRouter("MRS1", lo_addresses=[europe_ipv6 + "000::/64", MRS_ipv4 + "128/32"])
        MRS2 = self.addRouter("MRS2", lo_addresses=[europe_ipv6 + "100::/64", MRS_ipv4 + "64/32"])
         #routers of PAR
        PAR1 = self.addRouter("PAR1", lo_addresses=[europe_ipv6 + "200::/64", PAR_ipv4 + "128/32"])
        PAR2 = self.addRouter("PAR2", lo_addresses=[europe_ipv6 + "300::/64", PAR_ipv4 + "64/32"])
        # routers of SIN
        SIN1 = self.addRouter("SIN1", lo_addresses=[asia_ipv6 + "000::/64", SIN_ipv4 + "128/32"])
        SIN2 = self.addRouter("SIN2", lo_addresses=[asia_ipv6 + "100::/64", SIN_ipv4 + "64/32"])
        # routers of SYD
        SYD1 = self.addRouter("SYD1", lo_addresses=[asia_ipv6 + "200::/64", SYD_ipv4 + "128/32"])
        SYD2 = self.addRouter("SYD2", lo_addresses=[asia_ipv6 + "300::/64", SYD_ipv4 + "64/32"])
        # routers of LAX
        LAX1 = self.addRouter("LAX1", lo_addresses=[NA_ipv6 + "000::/64", LAX_ipv4 + "128/32"])
        LAX2 = self.addRouter("LAX2", lo_addresses=[NA_ipv6 + "100::/64", LAX_ipv4 + "64/32"])
        # routers of SJO
        SJO1 = self.addRouter("SJO1", lo_addresses=[NA_ipv6 + "200::/64", SJO_ipv4 + "128/32"])
        SJO2 = self.addRouter("SJO2", lo_addresses=[NA_ipv6 + "300::/64", SJO_ipv4 + "64/32"])
        #routers of ASH
        ASH1 = self.addRouter("ASH1", lo_addresses=[NA_ipv6 + "400::/64", ASH_ipv4 + "128/32"])
        ASH2 = self.addRouter("ASH2", lo_addresses=[NA_ipv6 + "500::/64", ASH_ipv4 + "64/32"])
        #routers peering vodafone
        VDF_PAR2 = self.addRouter("VDF_PAR2", lo_addresses=["dead:beaf:0000:0000::/64", "174.50.0.0/32"])
        VDF_ASH1 = self.addRouter("VDF_ASH1", lo_addresses=["dead:beaf:0000:0001::/64", "174.50.0.1/32"])
        VDF_SIN1 = self.addRouter("VDF_SIN1", lo_addresses=["dead:beaf:0000:0002::/64", "174.50.0.2/32"])
        VDF_SIN2 = self.addRouter("VDF_SIN2", lo_addresses=["dead:beaf:0000:0002::/64", "174.50.0.2/32"])
        #routers peering equinix
        EQX_SIN1 = self.addRouter("EQX_SIN1", lo_addresses=["dead:beaf:0001:0000::/64", "174.50.1.0/32"])
        EQX_SYD2 = self.addRouter("EQX_SYD2", lo_addresses=["dead:beaf:0001:0001::/64", "174.50.1.1/32"])
        #routers peering NTT
        NTT_SYD1 = self.addRouter("NTT_SYD1", lo_addresses=["dead:beaf:0002:0000::/64", "174.50.2.0/32"])
        
        
        
        # adding OSPF6 as IGP
        #=========================================================
        MRS1.addDaemon(OSPF6)
        MRS2.addDaemon(OSPF6)

        SIN1.addDaemon(OSPF6)
        SIN2.addDaemon(OSPF6)

        SYD1.addDaemon(OSPF6)
        SYD2.addDaemon(OSPF6)

        LAX1.addDaemon(OSPF6)        
        LAX2.addDaemon(OSPF6)

        SJO1.addDaemon(OSPF6)
        SJO2.addDaemon(OSPF6)

        ASH1.addDaemon(OSPF6)
        ASH2.addDaemon(OSPF6)

        PAR1.addDaemon(OSPF6)
        PAR2.addDaemon(OSPF6)

        VDF_PAR2.addDaemon(OSPF6)
        VDF_ASH1.addDaemon(OSPF6)
        VDF_SIN1.addDaemon(OSPF6)
        VDF_SIN2.addDaemon(OSPF6)

        EQX_SIN1.addDaemon(OSPF6)
        EQX_SYD2.addDaemon(OSPF6)

        NTT_SYD1.addDaemon(OSPF6)

        # adding BGP 
        #=========================================================
        MRS1.addDaemon(BGP)
        MRS2.addDaemon(BGP)

        SIN1.addDaemon(BGP)
        SIN2.addDaemon(BGP)

        SYD1.addDaemon(BGP)
        SYD2.addDaemon(BGP)

        LAX1.addDaemon(BGP)        
        LAX2.addDaemon(BGP)

        SJO1.addDaemon(BGP)
        SJO2.addDaemon(BGP)

        ASH1.addDaemon(BGP)
        ASH2.addDaemon(BGP)

        PAR1.addDaemon(BGP)
        PAR2.addDaemon(BGP)

        VDF_PAR2.addDaemon(BGP)
        VDF_ASH1.addDaemon(BGP)
        VDF_SIN1.addDaemon(BGP)
        VDF_SIN2.addDaemon(BGP)

        EQX_SIN1.addDaemon(BGP)
        EQX_SYD2.addDaemon(BGP)

        NTT_SYD1.addDaemon(BGP)


        

        #add firewall to the affected routers
        #=========================================================
        
        #rules for the routers
        ip_rules = [Rule("-A INPUT -s 1627:6100::/32 -j REJECT"),
        Rule("-A OUTPUT -d 1627:6100::/32 -j REJECT")]

        #adding to the routers
        SIN1.addDaemon(IP6Tables, rules=ip_rules)
        SIN2.addDaemon(IP6Tables, rules=ip_rules)
        SYD1.addDaemon(IP6Tables, rules=ip_rules)
        SYD2.addDaemon(IP6Tables, rules=ip_rules)
        ASH1.addDaemon(IP6Tables, rules=ip_rules)
        PAR2.addDaemon(IP6Tables, rules=ip_rules)
        




        # linkin twin datacenters10.12.0.1
        #=========================================================

        l_MRS1_MRS2 = self.addLink(MRS1, MRS2)
        l_MRS1_MRS2[MRS1].addParams(ip=(europe_ipv6 + "00a::1/64", MRS_ipv4 + "129/30"))
        l_MRS1_MRS2[MRS2].addParams(ip=(europe_ipv6 + "00a::2/64", MRS_ipv4 + "130/30"))

        l_SIN1_SIN2 = self.addLink(SIN1, SIN2)
        l_SIN1_SIN2[SIN1].addParams(ip=(asia_ipv6 + "00a::1/64", SIN_ipv4 + "129/30"))
        l_SIN1_SIN2[SIN2].addParams(ip=(asia_ipv6 + "00a::2/64", SIN_ipv4 + "130/30"))

        l_SYD1_SYD2 = self.addLink(SYD1, SYD2)
        l_SYD1_SYD2[SYD1].addParams(ip=(asia_ipv6 + "00c::1/64", SYD_ipv4 + "129/30"))
        l_SYD1_SYD2[SYD1].addParams(ip=(asia_ipv6 + "00c::2/64", SYD_ipv4 + "130/30"))

        l_PAR1_PAR2 = self.addLink(PAR1, PAR2)
        l_PAR1_PAR2[PAR1].addParams(ip=(europe_ipv6 + "00b::1/64", PAR_ipv4 + "129/30"))
        l_PAR1_PAR2[PAR2].addParams(ip=(europe_ipv6 + "00b::2/64", PAR_ipv4 + "130/30"))

        l_ASH1_ASH2 = self.addLink(ASH1, ASH2)
        l_ASH1_ASH2[ASH1].addParams(ip=(NA_ipv6 + "00a::1/64", ASH_ipv4 + "129/30"))
        l_ASH1_ASH2[ASH2].addParams(ip=(NA_ipv6 + "00a::2/64", ASH_ipv4 + "130/30"))

        l_LAX1_LAX2 = self.addLink(LAX1, LAX2)
        l_LAX1_LAX2[LAX1].addParams(ip=(NA_ipv6 + "00b::1/64", LAX_ipv4 + "129/30"))
        l_LAX1_LAX2[LAX2].addParams(ip=(NA_ipv6 + "00b::2/64", LAX_ipv4 + "130/30"))

        l_SJO1_SJO2 = self.addLink(SJO1, SJO2)
        l_SJO1_SJO2[SJO1].addParams(ip=(NA_ipv6 + "00c::1/64", SJO_ipv4 + "129/30"))
        l_SJO1_SJO2[SJO2].addParams(ip=(NA_ipv6 + "00c::2/64", SJO_ipv4 + "130/30"))

        #=========================================================

        l_MRS1_SIN1 = self.addLink(MRS1, SIN1)
        l_MRS1_SIN1[MRS1].addParams(ip=(europe_ipv6 + "011::1/64", MRS_ipv4 + "5/30"))
        l_MRS1_SIN1[SIN1].addParams(ip=(europe_ipv6 + "011::2/64", MRS_ipv4 + "6/30"))

        l_MRS2_SIN2 = self.addLink(MRS2, SIN2)
        l_MRS2_SIN2[MRS2].addParams(ip=(europe_ipv6 + "022::1/64", MRS_ipv4 + "9/30"))
        l_MRS2_SIN2[SIN2].addParams(ip=(europe_ipv6 + "022::2/64", MRS_ipv4 + "10/30"))

        l_SIN1_SYD1 = self.addLink(SIN1, SYD1)
        l_SIN1_SYD1[SIN1].addParams(ip=(asia_ipv6 + "011::1/64", SIN_ipv4 + "5/30"))
        l_SIN1_SYD1[SYD1].addParams(ip=(asia_ipv6 + "011::2/64", SIN_ipv4 + "6/30"))

        l_SIN2_SYD2 = self.addLink(SIN2, SYD2)
        l_SIN2_SYD2[SIN2].addParams(ip=(asia_ipv6 + "022::1/64", SIN_ipv4 + "9/30"))
        l_SIN2_SYD2[SYD2].addParams(ip=(asia_ipv6 + "022::2/64", SIN_ipv4 + "10/30"))

        l_SIN2_SJO1 = self.addLink(SIN2, SJO1)
        l_SIN2_SJO1[SIN2].addParams(ip=(asia_ipv6 + "021::1/64", SIN_ipv4 + "17/30"))
        l_SIN2_SJO1[SJO1].addParams(ip=(asia_ipv6 + "021::2/64", SIN_ipv4 + "18/30"))

        l_SIN2_SJO2 = self.addLink(SIN2, SJO2)
        l_SIN2_SJO2[SIN2].addParams(ip=(asia_ipv6 + "220::1/64", SIN_ipv4 + "33/30"))
        l_SIN2_SJO2[SJO2].addParams(ip=(asia_ipv6 + "220::2/64", SIN_ipv4 + "34/30"))

        #=======================================================


        l_ASH1_LAX1 = self.addLink(ASH1, LAX1)
        l_ASH1_LAX1[ASH1].addParams(ip=(NA_ipv6 + "011::1/64", ASH_ipv4 + "5/30"))
        l_ASH1_LAX1[LAX1].addParams(ip=(NA_ipv6 + "011::2/64", ASH_ipv4 + "6/30"))

        l_ASH2_LAX2 = self.addLink(ASH2, LAX2)
        l_ASH2_LAX2[ASH2].addParams(ip=(NA_ipv6 + "022::1/64", ASH_ipv4 + "9/30"))
        l_ASH2_LAX2[LAX2].addParams(ip=(NA_ipv6 + "022::2/64", ASH_ipv4 + "10/30"))

        l_ASH1_LAX2 = self.addLink(ASH1, LAX2)
        l_ASH1_LAX2[ASH1].addParams(ip=(NA_ipv6 + "012::1/64", ASH_ipv4 + "17/30"))
        l_ASH1_LAX2[LAX2].addParams(ip=(NA_ipv6 + "012::2/64", ASH_ipv4 + "18/30"))

        l_SJO1_LAX1 = self.addLink(SJO1, LAX1)
        l_SJO1_LAX1[SJO1].addParams(ip=(NA_ipv6 + "110::1/64", SJO_ipv4 + "5/30"))
        l_SJO1_LAX1[LAX1].addParams(ip=(NA_ipv6 + "110::2/64", SJO_ipv4 + "6/30"))

        l_SJO2_LAX2 = self.addLink(SJO2,LAX2)
        l_SJO2_LAX2[SJO2].addParams(ip=(NA_ipv6 + "220::1/64", SJO_ipv4 + "9/30"))
        l_SJO2_LAX2[LAX2].addParams(ip=(NA_ipv6 + "220::2/64", SJO_ipv4 + "10/30"))

        l_PAR1_ASH1 = self.addLink(PAR1,ASH1)
        l_PAR1_ASH1[PAR1].addParams(ip=(europe_ipv6 + "110::1/64", PAR_ipv4 + "5/30"))
        l_PAR1_ASH1[ASH1].addParams(ip=(europe_ipv6 + "110::2/64", PAR_ipv4 + "6/30"))

        l_PAR2_ASH2 = self.addLink(PAR2,ASH2)
        l_PAR2_ASH2[PAR2].addParams(ip=(europe_ipv6 + "220::1/64", PAR_ipv4 + "9/30"))
        l_PAR2_ASH2[ASH2].addParams(ip=(europe_ipv6 + "220::2/64", PAR_ipv4 + "10/30"))

        l_PAR1_MRS1 = self.addLink(PAR1,MRS1)
        l_PAR1_MRS1[PAR1].addParams(ip=(europe_ipv6 + "101::1/64", PAR_ipv4 + "17/30"))
        l_PAR1_MRS1[MRS1].addParams(ip=(europe_ipv6 + "101::2/64", PAR_ipv4 + "18/30"))

        l_PAR2_MRS2 = self.addLink(PAR2, MRS2)
        l_PAR2_MRS2[PAR2].addParams(ip=(europe_ipv6 + "202::1/64", PAR_ipv4 + "33/30"))
        l_PAR2_MRS2[MRS2].addParams(ip=(europe_ipv6 + "202::2/64", PAR_ipv4 + "34/30"))

        l_SYD2_LAX2 = self.addLink(SYD2,LAX2)
        l_SYD2_LAX2[SYD2].addParams(ip=(europe_ipv6 + "303::/64", SYD_ipv4 + "5/30"))
        l_SYD2_LAX2[LAX2].addParams(ip=(europe_ipv6 + "103::/64", SYD_ipv4 + "6/30"))

        l_VDF_PAR2 = self.addLink(VDF_PAR2, PAR2)
        l_VDF_PAR2[VDF_PAR2].addParams(ip=(peer_ipv6 + "011::1/64", ))

        l_VDF_ASH1 = self.addLink(VDF_ASH1,ASH1)

        l_VDF_SIN1 = self.addLink(VDF_SIN1, SIN1)

        l_VDF_SIN2 = self.addLink(VDF_SIN2, SIN2)

        l_EQX_SIN1 = self.addLink(EQX_SIN1, SIN1)

        l_EQX_SYD2 = self.addLink(EQX_SYD2, SYD2)

        l_NTT_SYD1 = self.addLink(NTT_SYD1, SYD1)

        H1 = self.addHost("H1")
        H2 = self.addHost("H2")

        l_H1_PAR1 = self.addLink(H1, PAR1)
        l_H1_PAR1[PAR1].addParams(ip=(europe_ipv6 + "20a::2/64", PAR_ipv4 + "69/30"))
        l_H1_PAR1[H1].addParams(ip=(europe_ipv6 + "20a::a/64", PAR_ipv4 + "70/30"))

        l_H2_SIN1 = self.addLink(H2, SIN1)
        l_H2_SIN1[SIN1].addParams(ip=(asia_ipv6 + "00a::0/64", SIN_ipv4 + "69/30"))
        l_H2_SIN1[H2].addParams(ip=(asia_ipv6 + "00a::a/64", SIN_ipv4 + "70/30"))
    
        super().build(*args, **kwargs)


# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=SimpleBGPTopo(), allocate_IPs = False)
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
