#!/usr/bin/env python3

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, OSPF6, OSPF, RouterConfig, AF_INET6, AF_INET, set_rr, ebgp_session, SHARE, IP6Tables, InputFilter, Deny, Allow, Rule, bgp_fullmesh, bgp_peering, ebgp_session
import hashlib


monde_ipv6 = "1627:6000:0000"
europe_ipv6 = monde_ipv6 + ":0"
NA_ipv6 = monde_ipv6 + ":1"
asia_ipv6 = monde_ipv6 + ":2"
server_ipv6 = monde_ipv6 + ":3"
server_ipv4 = "162.76.7."

MRS_ipv4 = "162.76.0."
PAR_ipv4 = "162.76.1."
SIN_ipv4 = "162.76.2."
SYD_ipv4 = "162.76.3."
LAX_ipv4 = "162.76.4."
SJO_ipv4 = "162.76.5."
ASH_ipv4 = "162.76.6."


VDF_ipv4 = "160.76.7."
EQX_ipv4 = "160.76.8."
NTT_ipv4 = "160.76.9."
VDF_ipv6 = "1627:6100:0000:0"
EQX_ipv6 = "1627:6200:0000:0"
NTT_ipv6 = "1627:6300:0000:0"

def createPassword(key):
    hash_object = hashlib.sha256(bytes(key, encoding='utf-8'))
    return hash_object.hexdigest()
    
secretKey = "Nu798SHkJ6MRwm69rZvu"
VDF_PW = createPassword("VDF"+secretKey)
EQX_PW = createPassword("EQX"+secretKey)
NTT_PW = createPassword("NTT"+secretKey)
SERVER_PW = createPassword("SER"+secretKey)





class SimpleBGPTopo(IPTopo):
    
    def build(self, *args, **kwargs):

       
        # first step, adding routers
        #=========================================================
       
        # routers of MRS
        MRS1 = self.addRouter("MRS1",config=RouterConfig, lo_addresses=[europe_ipv6 + "000::/64", MRS_ipv4 + "253/32"])
        MRS2 = self.addRouter("MRS2",config=RouterConfig, lo_addresses=[europe_ipv6 + "100::/64", MRS_ipv4 + "254/32"])
         #routers of PAR
        PAR1 = self.addRouter("PAR1",config=RouterConfig, lo_addresses=[europe_ipv6 + "200::/64", PAR_ipv4 + "253/32"])
        PAR2 = self.addRouter("PAR2",config=RouterConfig, lo_addresses=[europe_ipv6 + "300::/64", PAR_ipv4 + "254/32"])
        # routers of SIN
        SIN1 = self.addRouter("SIN1",config=RouterConfig, lo_addresses=[asia_ipv6 + "000::/64", SIN_ipv4 + "253/32"])
        SIN2 = self.addRouter("SIN2",config=RouterConfig, lo_addresses=[asia_ipv6 + "100::/64", SIN_ipv4 + "254/32"])
        # routers of SYD
        SYD1 = self.addRouter("SYD1",config=RouterConfig, lo_addresses=[asia_ipv6 + "200::/64", SYD_ipv4 + "253/32"])
        SYD2 = self.addRouter("SYD2",config=RouterConfig, lo_addresses=[asia_ipv6 + "300::/64", SYD_ipv4 + "254/32"])
        # routers of LAX
        LAX1 = self.addRouter("LAX1",config=RouterConfig, lo_addresses=[NA_ipv6 + "000::/64", LAX_ipv4 + "253/32"])
        LAX2 = self.addRouter("LAX2",config=RouterConfig, lo_addresses=[NA_ipv6 + "100::/64", LAX_ipv4 + "254/32"])
        # routers of SJO
        SJO1 = self.addRouter("SJO1",config=RouterConfig, lo_addresses=[NA_ipv6 + "200::/64", SJO_ipv4 + "253/32"])
        SJO2 = self.addRouter("SJO2",config=RouterConfig, lo_addresses=[NA_ipv6 + "300::/64", SJO_ipv4 + "254/32"])
        #routers of ASH
        ASH1 = self.addRouter("ASH1",config=RouterConfig, lo_addresses=[NA_ipv6 + "400::/64", ASH_ipv4 + "253/32"])
        ASH2 = self.addRouter("ASH2", config=RouterConfig,lo_addresses=[NA_ipv6 + "500::/64", ASH_ipv4 + "254/32"])
        #routers peering vodafone
        VDF = self.addRouter("VDF",config=RouterConfig, lo_addresses=[VDF_ipv6 + "000::/64", VDF_ipv4 + "253/32"])
        #routers peering equinix
        EQX = self.addRouter("EQX",config=RouterConfig, lo_addresses=[EQX_ipv6 + "000::/64", EQX_ipv4 + "253/32"])
        #routers peering NTT
        NTT = self.addRouter("NTT",config=RouterConfig, lo_addresses=[NTT_ipv6 + "000::/64", NTT_ipv4 + "253/32"])
        
        
        
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
        
        VDF.addDaemon(OSPF6)
        EQX.addDaemon(OSPF6)
        NTT.addDaemon(OSPF6)

        # adding OSPF
        #=========================================================

        MRS1.addDaemon(OSPF)
        MRS2.addDaemon(OSPF)

        SIN1.addDaemon(OSPF)
        SIN2.addDaemon(OSPF)

        SYD1.addDaemon(OSPF)
        SYD2.addDaemon(OSPF)

        LAX1.addDaemon(OSPF)        
        LAX2.addDaemon(OSPF)

        SJO1.addDaemon(OSPF)
        SJO2.addDaemon(OSPF)

        ASH1.addDaemon(OSPF)
        ASH2.addDaemon(OSPF)

        PAR1.addDaemon(OSPF)
        PAR2.addDaemon(OSPF)

        VDF.addDaemon(OSPF)
        EQX.addDaemon(OSPF)
        NTT.addDaemon(OSPF)

        # adding BGP 
        #=========================================================
        MRS1.addDaemon(BGP,debug=("neighbor",))
        MRS2.addDaemon(BGP,debug=("neighbor",))

        SIN1.addDaemon(BGP,debug=("neighbor",))
        SIN2.addDaemon(BGP,debug=("neighbor",))

        SYD1.addDaemon(BGP,debug=("neighbor",))
        SYD2.addDaemon(BGP,debug=("neighbor",))

        LAX1.addDaemon(BGP,debug=("neighbor",))       
        LAX2.addDaemon(BGP,debug=("updates",))

        SJO1.addDaemon(BGP,debug=("updates",))
        SJO2.addDaemon(BGP,debug=("updates",))

        ASH1.addDaemon(BGP,debug=("updates",))
        ASH2.addDaemon(BGP,debug=("updates",))

        PAR1.addDaemon(BGP,debug=("updates",))
        PAR2.addDaemon(BGP,debug=("updates",))

        VDF.addDaemon(BGP,config=RouterConfig,address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected']),),debug=("updates",))
        EQX.addDaemon(BGP,config=RouterConfig,address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected']),),debug=("updates",))
        NTT.addDaemon(BGP,config=RouterConfig,address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected']),),debug=("updates",))

      
        # linkin twin datacenters
        #=========================================================
        l_MRS1_MRS2 = self.addLink(MRS1,MRS2,igp_metric=2)
        l_MRS1_MRS2[MRS1].addParams(ip=(europe_ipv6 + "00a::1/64", MRS_ipv4 + "129/30"))
        l_MRS1_MRS2[MRS2].addParams(ip=(europe_ipv6 + "00a::2/64", MRS_ipv4 + "130/30"))

        l_SIN1_SIN2 = self.addLink(SIN1,SIN2,igp_metric=2)
        l_SIN1_SIN2[SIN1].addParams(ip=(asia_ipv6 + "00a::1/64", SIN_ipv4 + "129/30"))
        l_SIN1_SIN2[SIN2].addParams(ip=(asia_ipv6 + "00a::2/64", SIN_ipv4 + "130/30"))

        l_SYD1_SYD2 = self.addLink(SYD1,SYD2,igp_metric=2)
        l_SYD1_SYD2[SYD1].addParams(ip=(asia_ipv6 + "00c::1/64", SYD_ipv4 + "129/30"))
        l_SYD1_SYD2[SYD2].addParams(ip=(asia_ipv6 + "00c::2/64", SYD_ipv4 + "130/30"))

        l_PAR1_PAR2 = self.addLink(PAR1,PAR2,igp_metric=2)
        l_PAR1_PAR2[PAR1].addParams(ip=(europe_ipv6 + "00b::1/64", PAR_ipv4 + "129/30"))
        l_PAR1_PAR2[PAR2].addParams(ip=(europe_ipv6 + "00b::2/64", PAR_ipv4 + "130/30"))

        l_ASH1_ASH2 = self.addLink(ASH1, ASH2,igp_metric=2)
        l_ASH1_ASH2[ASH1].addParams(ip=(NA_ipv6 + "00a::1/64", ASH_ipv4 + "129/30"))
        l_ASH1_ASH2[ASH2].addParams(ip=(NA_ipv6 + "00a::2/64", ASH_ipv4 + "130/30"))

        l_LAX1_LAX2 = self.addLink(LAX1, LAX2,igp_metric=2)
        l_LAX1_LAX2[LAX1].addParams(ip=(NA_ipv6 + "00b::1/64", LAX_ipv4 + "129/30"))
        l_LAX1_LAX2[LAX2].addParams(ip=(NA_ipv6 + "00b::2/64", LAX_ipv4 + "130/30"))

        l_SJO1_SJO2 = self.addLink(SJO1, SJO2,igp_metric=2)
        l_SJO1_SJO2[SJO1].addParams(ip=(NA_ipv6 + "00c::1/64", SJO_ipv4 + "129/30"))
        l_SJO1_SJO2[SJO2].addParams(ip=(NA_ipv6 + "00c::2/64", SJO_ipv4 + "130/30"))

        #=========================================================

        l_MRS1_SIN1 = self.addLink(MRS1, SIN1,igp_metric=10)
        l_MRS1_SIN1[MRS1].addParams(ip=(europe_ipv6 + "011::1/64", MRS_ipv4 + "5/30"))
        l_MRS1_SIN1[SIN1].addParams(ip=(europe_ipv6 + "011::2/64", MRS_ipv4 + "6/30"))

        l_MRS2_SIN2 = self.addLink(MRS2, SIN2,igp_metric=10)
        l_MRS2_SIN2[MRS2].addParams(ip=(europe_ipv6 + "022::1/64", MRS_ipv4 + "9/30"))
        l_MRS2_SIN2[SIN2].addParams(ip=(europe_ipv6 + "022::2/64", MRS_ipv4 + "10/30"))

        l_SIN1_SYD1 = self.addLink(SIN1, SYD1,igp_metric=3)
        l_SIN1_SYD1[SIN1].addParams(ip=(asia_ipv6 + "011::1/64", SIN_ipv4 + "5/30"))
        l_SIN1_SYD1[SYD1].addParams(ip=(asia_ipv6 + "011::2/64", SIN_ipv4 + "6/30"))

        l_SIN2_SYD2 = self.addLink(SIN2, SYD2,igp_metric=3)
        l_SIN2_SYD2[SIN2].addParams(ip=(asia_ipv6 + "022::1/64", SIN_ipv4 + "9/30"))
        l_SIN2_SYD2[SYD2].addParams(ip=(asia_ipv6 + "022::2/64", SIN_ipv4 + "10/30"))

        l_SIN2_SJO1 = self.addLink(SIN2, SJO1,igp_metric=10)
        l_SIN2_SJO1[SIN2].addParams(ip=(asia_ipv6 + "021::1/64", SIN_ipv4 + "17/30"))
        l_SIN2_SJO1[SJO1].addParams(ip=(asia_ipv6 + "021::2/64", SIN_ipv4 + "18/30"))

        l_SIN1_SJO2 = self.addLink(SIN1, SJO2,igp_metric=10)
        l_SIN1_SJO2[SIN1].addParams(ip=(asia_ipv6 + "220::1/64", SIN_ipv4 + "33/30"))
        l_SIN1_SJO2[SJO2].addParams(ip=(asia_ipv6 + "220::2/64", SIN_ipv4 + "34/30"))

        #=======================================================


        l_ASH1_LAX1 = self.addLink(ASH1, LAX1,igp_metric=3)
        l_ASH1_LAX1[ASH1].addParams(ip=(NA_ipv6 + "011::1/64", ASH_ipv4 + "5/30"))
        l_ASH1_LAX1[LAX1].addParams(ip=(NA_ipv6 + "011::2/64", ASH_ipv4 + "6/30"))

        l_ASH2_LAX2 = self.addLink(ASH2, LAX2,igp_metric=3)
        l_ASH2_LAX2[ASH2].addParams(ip=(NA_ipv6 + "022::1/64", ASH_ipv4 + "9/30"))
        l_ASH2_LAX2[LAX2].addParams(ip=(NA_ipv6 + "022::2/64", ASH_ipv4 + "10/30"))

        l_ASH1_LAX2 = self.addLink(ASH1, LAX2,igp_metric=10)
        l_ASH1_LAX2[ASH1].addParams(ip=(NA_ipv6 + "012::1/64", ASH_ipv4 + "17/30"))
        l_ASH1_LAX2[LAX2].addParams(ip=(NA_ipv6 + "012::2/64", ASH_ipv4 + "18/30"))

        l_SJO1_LAX1 = self.addLink(SJO1, LAX1,igp_metric=10)
        l_SJO1_LAX1[SJO1].addParams(ip=(NA_ipv6 + "110::1/64", SJO_ipv4 + "5/30"))
        l_SJO1_LAX1[LAX1].addParams(ip=(NA_ipv6 + "110::2/64", SJO_ipv4 + "6/30"))

        l_SJO2_LAX2 = self.addLink(SJO2,LAX2,igp_metric=10)
        l_SJO2_LAX2[SJO2].addParams(ip=(NA_ipv6 + "220::1/64", SJO_ipv4 + "9/30"))
        l_SJO2_LAX2[LAX2].addParams(ip=(NA_ipv6 + "220::2/64", SJO_ipv4 + "10/30"))

        l_PAR1_ASH1 = self.addLink(PAR1,ASH1, igp_metric=10)
        l_PAR1_ASH1[PAR1].addParams(ip=(europe_ipv6 + "110::1/64", PAR_ipv4 + "5/30"))
        l_PAR1_ASH1[ASH1].addParams(ip=(europe_ipv6 + "110::2/64", PAR_ipv4 + "6/30"))

        l_PAR2_ASH2 = self.addLink(PAR2,ASH2,igp_metric=10)
        l_PAR2_ASH2[PAR2].addParams(ip=(europe_ipv6 + "220::1/64", PAR_ipv4 + "9/30"))
        l_PAR2_ASH2[ASH2].addParams(ip=(europe_ipv6 + "220::2/64", PAR_ipv4 + "10/30"))

        l_PAR1_MRS2 = self.addLink(PAR1,MRS2,igp_metric=3)
        l_PAR1_MRS2[PAR1].addParams(ip=(europe_ipv6 + "101::1/64", PAR_ipv4 + "17/30"))
        l_PAR1_MRS2[MRS2].addParams(ip=(europe_ipv6 + "101::2/64", PAR_ipv4 + "18/30"))

        l_PAR2_MRS1 = self.addLink(PAR2, MRS1,igp_metric=10)
        l_PAR2_MRS1[PAR2].addParams(ip=(europe_ipv6 + "202::1/64", PAR_ipv4 + "33/30"))
        l_PAR2_MRS1[MRS1].addParams(ip=(europe_ipv6 + "202::2/64", PAR_ipv4 + "34/30"))

        l_SYD2_LAX2 = self.addLink(SYD2,LAX2,igp_metric=10)
        l_SYD2_LAX2[SYD2].addParams(ip=(europe_ipv6 + "303::1/64", SYD_ipv4 + "5/30"))
        l_SYD2_LAX2[LAX2].addParams(ip=(europe_ipv6 + "303::2/64", SYD_ipv4 + "6/30"))

        #=============================================================================
        #Peering links

        l_VDF_PAR2 = self.addLink(VDF, PAR2,igp_metric=10)
        l_VDF_PAR2[VDF].addParams(ip=(europe_ipv6 + "ffa::1/64",PAR_ipv4 + "73/30"))
        l_VDF_PAR2[PAR2].addParams(ip=(europe_ipv6 + "ffa::2/64",PAR_ipv4 + "74/30"))

        l_VDF_ASH1 = self.addLink(VDF,ASH1,igp_metric=10)
        l_VDF_ASH1[VDF].addParams(ip=(NA_ipv6 + "ffa::1/64",ASH_ipv4 + "73/30"))
        l_VDF_ASH1[ASH1].addParams(ip=(NA_ipv6 + "ffa::2/64",ASH_ipv4 + "74/30"))

        l_VDF_SIN1 = self.addLink(VDF, SIN1,igp_metric=10)
        l_VDF_SIN1[VDF].addParams(ip=(asia_ipv6 + "ffa::1/64",SIN_ipv4 + "73/30"))
        l_VDF_SIN1[SIN1].addParams(ip=(asia_ipv6 + "ffa::2/64",SIN_ipv4 + "74/30"))

        l_VDF_SIN2 = self.addLink(VDF, SIN2,igp_metric=10)
        l_VDF_SIN2[VDF].addParams(ip=(asia_ipv6 + "1fa::1/64",SIN_ipv4 + "81/30"))
        l_VDF_SIN2[SIN2].addParams(ip=(asia_ipv6 + "1fa::2/64",SIN_ipv4 + "82/30"))

        l_EQX_SIN1 = self.addLink(EQX, SIN1,igp_metric=10)
        l_EQX_SIN1[EQX].addParams(ip=(asia_ipv6 + "2fb::1/64",SIN_ipv4 + "89/30"))
        l_EQX_SIN1[SIN1].addParams(ip=(asia_ipv6 + "2fb::2/64",SIN_ipv4 + "90/30"))

        l_EQX_SYD2 = self.addLink(EQX, SYD2,igp_metric=10)
        l_EQX_SYD2[EQX].addParams(ip=(asia_ipv6 + "3fa::1/64",SYD_ipv4 + "73/30"))
        l_EQX_SYD2[SYD2].addParams(ip=(asia_ipv6 + "3fa::2/64",SYD_ipv4 + "74/30"))

        l_NTT_SYD2 = self.addLink(NTT, SYD2,igp_metric=10)
        l_NTT_SYD2[NTT].addParams(ip=(asia_ipv6 + "4fb::1/64",SYD_ipv4 + "81/30"))
        l_NTT_SYD2[SYD2].addParams(ip=(asia_ipv6 + "4fb::2/64",SYD_ipv4 + "82/30"))

        l_NTT_SYD1 = self.addLink(NTT, SYD1,igp_metric=10)
        l_NTT_SYD1[NTT].addParams(ip=(asia_ipv6 + "5fa::1/64",SYD_ipv4 + "89/30"))
        l_NTT_SYD1[SYD1].addParams(ip=(asia_ipv6 + "5fa::2/64",SYD_ipv4 + "90/30"))


        #=============================================================================
        #servers

        S1 = self.addRouter("S1", config=RouterConfig, lo_addresses=[server_ipv6 + "::/64", server_ipv4 + "1/32"])
        S2 = self.addRouter("S2", config=RouterConfig, lo_addresses=[server_ipv6 + "::/64", server_ipv4 + "1/32"])

        #Adding BGP daemons to manage failures

        S1.addDaemon(BGP,address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected'])))
        S2.addDaemon(BGP,address_families=(AF_INET6(redistribute=['connected']),AF_INET(redistribute=['connected'])))

        # S1.addDaemon(OSPF6)
        # S2.addDaemon(OSPF6)
        
        self.addAS(64512, (S1,))
        self.addAS(64512, (S2,))

        l_S1_SJO1 = self.addLink(S1,SJO1, igp_metric=3)
        l_S1_SJO1[S1].addParams(ip=(server_ipv6 + "a1a::1/64",server_ipv4 + "5/30"))
        l_S1_SJO1[SJO1].addParams(ip=(server_ipv6 + "a1a::2/64",server_ipv4 + "6/30"))

        l_S2_PAR1 = self.addLink(S2,PAR1, igp_metric=3)
        l_S2_PAR1[S2].addParams(ip=(server_ipv6 + "a1a::3/64",server_ipv4 + "9/30"))
        l_S2_PAR1[PAR1].addParams(ip=(server_ipv6 + "a1a::4/64",server_ipv4 + "10/30"))

        ebgp_session(self,S1, SJO1)
        ebgp_session(self,S2, PAR1)
        

        #=============================================================================
        # BGP setup
        self.addAS(1,(MRS1,MRS2,PAR1,PAR2,SIN1,SIN2,SYD1,SYD2,SJO1,SJO2,LAX1,LAX2,ASH1,ASH2))
        set_rr(self, rr=SIN1, peers=[SYD1, MRS1, SIN2, MRS2, SJO1, SJO2])
        set_rr(self, rr=SYD2, peers=[SYD1, SIN2, SJO1, LAX1, LAX2])
        set_rr(self, rr=ASH1, peers=[SJO1, SJO2, LAX1, LAX2, PAR1, ASH2])
        set_rr(self, rr=PAR2, peers=[MRS1, MRS2, PAR1, ASH2])
        bgp_fullmesh(self, [SIN1, SYD2, ASH1, PAR2])
        # bgp_fullmesh(self, [MRS1,MRS2,PAR1,PAR2,SIN1,SIN2,SYD1,SYD2,SJO1,SJO2,LAX1,LAX2,ASH1,ASH2])
       
        self.addAS(2, (EQX,))
        self.addAS(3, (VDF,))
        self.addAS(4, (NTT,))

        ebgp_session(self, VDF, PAR2)
        ebgp_session(self, VDF, ASH1)
        ebgp_session(self, VDF, SIN1)
        ebgp_session(self, VDF, SIN2)
        ebgp_session(self, EQX, SIN1)
        ebgp_session(self, EQX, SYD2)
        ebgp_session(self, NTT, SYD2)
        ebgp_session(self, NTT, SYD1)


        H1 = self.addHost("H1")
        H2 = self.addHost("H2")
        H3 = self.addHost("H3")
        


        l_H1_VDF = self.addLink(H1, VDF,igp_metric=2)
        l_H1_VDF[H1].addParams(ip=(europe_ipv6 + "aaa::2/64", VDF_ipv4 + "5/30"))
        l_H1_VDF[VDF].addParams(ip=(europe_ipv6 + "aaa::a/64", VDF_ipv4 + "6/30"))

        l_H2_EQX = self.addLink(H2, EQX,igp_metric=2)
        l_H2_EQX[H2].addParams(ip=(europe_ipv6 + "bbb::2/64", EQX_ipv4 + "9/30"))
        l_H2_EQX[EQX].addParams(ip=(europe_ipv6 + "bbb::a/64", EQX_ipv4 + "10/30"))

        l_H3_NTT = self.addLink(H3, NTT,igp_metric=2)
        l_H3_NTT[H3].addParams(ip=(europe_ipv6 + "ccc::2/64", NTT_ipv4 + "17/30"))
        l_H3_NTT[NTT].addParams(ip=(europe_ipv6 + "ccc::a/64", NTT_ipv4 + "18/30"))


        #=============================================================================
        #communities set up


        super().build(*args, **kwargs)


# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=SimpleBGPTopo(), allocate_IPs = False)
    try:
        net.start()
        ########################################
        #Configuring server to respond faster to failures
        print(net['PAR1'].cmd('python3 scripts/BGP_V6_KALIVE_TIMEOUT.py {} {} {}'.format("1627:6000:0:3a1a::3",1,4)))
        print(net['S2'].cmd('python3 scripts/BGP_V6_KALIVE_TIMEOUT.py {} {} {}'.format("1627:6000:0:3a1a::4",1,4)))

        #Configuring TTL and PASSWORD for PAR1-S2
        print(net['PAR1'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format("1627:6000:0:3a1a::3",2,SERVER_PW)))
        print(net['S2'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format("1627:6000:0:3a1a::4",2,SERVER_PW)))
        
        #Configuring TTL and PASSWORD for SIN1-EQX
        print(net['EQX'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "2fb::2",2,EQX_PW)))
        print(net['SIN1'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "2fb::1",2,EQX_PW)))

        #Configuring TTL and PASSWORD for SYD2-NTT
        print(net['NTT'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "4fb::2",2,NTT_PW)))
        print(net['SYD2'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(asia_ipv6 + "4fb::1",2,NTT_PW)))

        #Configuring TTL and PASSWORD for PAR2-VDF
        print(net['VDF'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(europe_ipv6 + "ffa::2",2,VDF_PW)))
        print(net['PAR2'].cmd('python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'.format(europe_ipv6 + "ffa::1",2,VDF_PW)))
        ########################################


        ########################################
        #Defining communities
        community_as_prepend_x1 = "1:100"
        community_as_prepend_x1_name = "prepend_x1"
        community_as_prepend_x2 = "2:100"
        community_as_prepend_x2_name = "prepend_x2"
        community_local_pref_200 = "200:200"
        community_local_pref_200_name = "local_pref_200"
        general_route_map = "general_route_map"
        #creating community lists
        print(net['SIN1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x1,community_as_prepend_x1_name)))
        print(net['SIN1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x2,community_as_prepend_x2_name)))
        print(net['SIN1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_local_pref_200,community_local_pref_200_name)))
        #Adding prepend X1
        print(net['SIN1'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x1_name,general_route_map,10)))
        #Adding prepend X2
        print(net['SIN1'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x2_name,general_route_map,20)))
        #Adding local-pref 200
        print(net['SIN1'].cmd('python3 scripts/BGP_COMML_LPREF_RMNAME_SEQ.py {} {} {} {}'.format(community_local_pref_200_name, 200, general_route_map,30)))
        #Adding default permit at the end
        print(net['SIN1'].cmd('python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map,100)))

        #applying route-map on neighbors
        print(net['SIN1'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(asia_ipv6 + "2fb::1",general_route_map,"in")))
        print(net['SIN1'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(asia_ipv6 + "ffa::1",general_route_map,"in")))
        
        #=================================#
        #=================================#

        print(net['SIN2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x1,community_as_prepend_x1_name)))
        print(net['SIN2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x2,community_as_prepend_x2_name)))
        print(net['SIN2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_local_pref_200,community_local_pref_200_name)))
        #Adding prepend X1
        print(net['SIN2'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x1_name,general_route_map,10)))
        #Adding prepend X2
        print(net['SIN2'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x2_name,general_route_map,20)))
        #Adding local-pref 200
        print(net['SIN2'].cmd('python3 scripts/BGP_COMML_LPREF_RMNAME_SEQ.py {} {} {} {}'.format(community_local_pref_200_name, 200, general_route_map,30)))
        #Adding default permit at the end
        print(net['SIN2'].cmd('python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map,100)))
        #applying route-map on neighbors
        print(net['SIN2'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(asia_ipv6 + "1fa::1",general_route_map,"in")))

        #=================================#
        #=================================#
        
        print(net['SYD1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x1,community_as_prepend_x1_name)))
        print(net['SYD1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x2,community_as_prepend_x2_name)))
        print(net['SYD1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_local_pref_200,community_local_pref_200_name)))
        #Adding prepend X1
        print(net['SYD1'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x1_name,general_route_map,10)))
        #Adding prepend X2
        print(net['SYD1'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x2_name,general_route_map,20)))
        #Adding local-pref 200
        print(net['SYD1'].cmd('python3 scripts/BGP_COMML_LPREF_RMNAME_SEQ.py {} {} {} {}'.format(community_local_pref_200_name, 200, general_route_map,30)))
        #Adding default permit at the end
        print(net['SYD1'].cmd('python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map,100)))
        #applying route-map on neighbors
        print(net['SYD1'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(asia_ipv6 + "5fa::1",general_route_map,"in")))

        #=================================#
        #=================================#

        print(net['SYD2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x1,community_as_prepend_x1_name)))
        print(net['SYD2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x2,community_as_prepend_x2_name)))
        print(net['SYD2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_local_pref_200,community_local_pref_200_name)))
        #Adding prepend X1
        print(net['SYD2'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x1_name,general_route_map,10)))
        #Adding prepend X2
        print(net['SYD2'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x2_name,general_route_map,20)))
        #Adding local-pref 200
        print(net['SYD2'].cmd('python3 scripts/BGP_COMML_LPREF_RMNAME_SEQ.py {} {} {} {}'.format(community_local_pref_200_name, 200, general_route_map,30)))
        #Adding default permit at the end
        print(net['SYD2'].cmd('python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map,100)))

        #applying route-map on neighbors
        print(net['SYD2'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(asia_ipv6 + "3fa::1",general_route_map,"in")))
        print(net['SYD2'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(asia_ipv6 + "4fb::1",general_route_map,"in")))

        #=================================#
        #=================================#
    
        print(net['ASH1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x1,community_as_prepend_x1_name)))
        print(net['ASH1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x2,community_as_prepend_x2_name)))
        print(net['ASH1'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_local_pref_200,community_local_pref_200_name)))
        #Adding prepend X1
        print(net['ASH1'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x1_name,general_route_map,10)))
        #Adding prepend X2
        print(net['ASH1'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x2_name,general_route_map,20)))
        #Adding local-pref 200
        print(net['ASH1'].cmd('python3 scripts/BGP_COMML_LPREF_RMNAME_SEQ.py {} {} {} {}'.format(community_local_pref_200_name, 200, general_route_map,30)))
        #Adding default permit at the end
        print(net['ASH1'].cmd('python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map,100)))
        #applying route-map on neighbors
        print(net['ASH1'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(NA_ipv6 + "ffa::1",general_route_map,"in")))

        #=================================#
        #=================================#
    
        print(net['PAR2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x1,community_as_prepend_x1_name)))
        print(net['PAR2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_as_prepend_x2,community_as_prepend_x2_name)))
        print(net['PAR2'].cmd('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(community_local_pref_200,community_local_pref_200_name)))
        #Adding prepend X1
        print(net['PAR2'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x1_name,general_route_map,10)))
        #Adding prepend X2
        print(net['PAR2'].cmd('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(community_as_prepend_x2_name,general_route_map,20)))
        #Adding local-pref 200
        print(net['PAR2'].cmd('python3 scripts/BGP_COMML_LPREF_RMNAME_SEQ.py {} {} {} {}'.format(community_local_pref_200_name, 200, general_route_map,30)))
        #Adding default permit at the end
        print(net['PAR2'].cmd('python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map,100)))
        #applying route-map on neighbors
        print(net['PAR2'].cmd('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(europe_ipv6 + "ffa::1",general_route_map,"in")))

        #=================================#
        #=================================#
        IPCLI(net)
    finally:
        net.stop()
