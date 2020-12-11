import hashlib


def createPassword(key):
    hash_object = hashlib.sha256(bytes(key, encoding='utf-8'))
    return hash_object.hexdigest()


secretKey = "Nu798SHkJ6MRwm69rZvu"
VDF_PW = createPassword("VDF"+secretKey)
EQX_PW = createPassword("EQX"+secretKey)
NTT_PW = createPassword("NTT"+secretKey)
SERVER_PW = createPassword("SER"+secretKey)

community_as_prepend_x1 = "1:100"
community_as_prepend_x1_name = "prepend_x1"
community_as_prepend_x2 = "2:100"
community_as_prepend_x2_name = "prepend_x2"
community_as_prepend_x3 = "3:100"
community_as_prepend_x3_name = "prepend_x3"


community_local_pref_80 = "80:80"
community_local_pref_80_name ="local_pref_80"
community_local_pref_200 = "200:200"
community_local_pref_200_name = "local_pref_200"

community_no_export_NA = "10:15"
community_no_export_EU = "20:15"
community_no_export_ASIA = "30:15"
community_no_export_NA_name = "no_export_NA"
community_no_export_EU_name = "no_export_EU"
community_no_export_ASIA_name = "no_export_ASIA"

general_route_map = "general_route_map"
general_route_map_2 = "general_route_map2"


def serverScript(network, servers, sRouters):
    script = 'python3 scripts/BGP_V6_KALIVE_TIMEOUT.py {} {} {}'
    route_map = 'rm_asn'
    script_deny = 'python3 scripts/BGP_deny_server_V6.py {}'
    script_rm_asn = 'python3 scripts/BGP_rm_aspath_ASN_RM_SEQ.py {} {} {}'
    if(len(servers) != len(sRouters)):
        print("""number of servers and routeurs doesn't match""")
        return
    for i in range(len(servers)):
        serverName = servers[i][0]
        routerName = sRouters[i][0]
        serverAddr = servers[i][1]
        routerAddr = sRouters[i][1]
        #removing private AS in AS-path
        network[routerName].pexec(script_rm_asn.format(64512,route_map,10))
        network[routerName].pexec(
            'python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(serverAddr, route_map, "in")
        )
        network[serverName].pexec(
            'route add -A inet6 default gw {}'.format(routerAddr))
        network[routerName].pexec(script_deny.format(serverAddr))
        network[serverName].pexec(script.format(routerAddr, 10, 35))
        network[routerName].pexec(script.format(serverAddr, 10, 35))


def ttlCmdSetup(network, routers):
    for r in routers:
        network[r].pexec('sysctl net.ipv6.conf.all.hop_limit=255')


def findPassword(peerName):
    if(peerName.find('EQX') != -1):
        return EQX_PW
    if(peerName.find('NTT') != -1):
        return NTT_PW
    if(peerName.find('VDF') != -1):
        return VDF_PW
    if(peerName.find('SER') != -1):
        return SERVER_PW


def applyCommunities(network, routerName, peerAddr, communities):
    seq = 10
    rm = 'rm'
    script = 'python3 scripts/BGP_SET_ANY_COMM_RMNAME_SEQ.py {} {} {}'
    for c in communities:
        network[routerName].pexec(script.format(c, rm, seq))
        seq += 10
    network[routerName].pexec(
        'python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(rm, seq))
    network[routerName].pexec('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(
        peerAddr, rm, "out"))


def ttlPasswordSetup(network, routers, peers):
    script = 'python3 scripts/BGP_V6_TTL_PASSWORD.py {} {} {}'
    if len(routers) != len(peers):
        print("""number of routers and peers doesn't match""")
    for i in range(len(routers)):
        routerName = routers[i][0]
        routerAddr = routers[i][1]
        peerName = peers[i][0]
        peerAddr = peers[i][1]
        network[routerName].pexec(script.format(
            peerAddr, 1, findPassword(peerName)))
        network[peerName].pexec(script.format(
            routerAddr, 1, findPassword(peerName)))


def communitiesSetup(network, routersName, peersListAddr, continents):
    # Defining communities
    for i in range(len(routersName)):
        name = routersName[i]
        # declaring communities
        network[name].pexec('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(
            community_as_prepend_x1, community_as_prepend_x1_name))
        network[name].pexec('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(
            community_as_prepend_x2, community_as_prepend_x2_name))
        network[name].pexec('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(
            community_as_prepend_x3, community_as_prepend_x3_name))
        network[name].pexec('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(
            community_local_pref_80, community_local_pref_80_name))
        network[name].pexec('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(
            community_local_pref_200, community_local_pref_200_name))
        # handling "don't export to" communities
        noExportCommunities(network, name, continents[i])
        # Adding prepend X1
        network[name].pexec('python3 scripts/BGP_PX1_COMML_RMNAME_SEQ.py {} {} {}'.format(
            community_as_prepend_x1_name, general_route_map_2, 20))
        # Adding prepend X2
        network[name].pexec('python3 scripts/BGP_PX2_COMML_RMNAME_SEQ.py {} {} {}'.format(
            community_as_prepend_x2_name, general_route_map_2, 30))
        # Adding prepend X3
        network[name].pexec('python3 scripts/BGP_PX3_COMML_RMNAME_SEQ.py {} {} {}'.format(
            community_as_prepend_x3_name, general_route_map_2, 40))
        # adding local-pref 80
        network[name].pexec('python3 scripts/BGP_COMML_LPREF_RMNAME_SEQ.py {} {} {} {}'.format(
            community_local_pref_80_name, 80, general_route_map, 10))
        # Adding local-pref 200
        network[name].pexec('python3 scripts/BGP_COMML_LPREF_RMNAME_SEQ.py {} {} {} {}'.format(
            community_local_pref_200_name, 200, general_route_map, 20))
        
        # Adding default permit at the end
        network[name].pexec(
            'python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map, 100))
        network[name].pexec(
            'python3 scripts/BGP_empty_permit_RMNAME_SEQ.py {} {}'.format(general_route_map_2, 100))
        for j in range(len(peersListAddr[i])):
            peerAddr = peersListAddr[i][j]
            network[name].pexec('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(
                peerAddr, general_route_map, "in"))
            network[name].pexec('python3 scripts/BGP_NEIGHBOR_RMAP_INOUT.py {} {} {}'.format(
                peerAddr, general_route_map_2, "out"))


def noExportCommunities(network, routersName, continent):
    if continent == 'EU':
        network[routersName].pexec('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(
            community_no_export_EU, community_no_export_EU_name))
        network[routersName].pexec('python3 scripts/BGP_deny_COMM_RM_SEQ.py {} {} {}'.format(
            community_no_export_EU_name, general_route_map_2, 10))
    elif continent == 'NA':
        network[routersName].pexec('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(
            community_no_export_NA, community_no_export_NA_name))
        network[routersName].pexec('python3 scripts/BGP_deny_COMM_RM_SEQ.py {} {} {}'.format(
            community_no_export_NA_name, general_route_map_2, 10))
    elif continent == 'ASIA':
        network[routersName].pexec('python3 scripts/BGP_ccl_COMM_NAME.py {} {}'.format(
            community_no_export_ASIA, community_no_export_ASIA_name))
        network[routersName].pexec('python3 scripts/BGP_deny_COMM_RM_SEQ.py {} {} {}'.format(
            community_no_export_ASIA_name, general_route_map_2, 10))
    else:
        print("""this continent doesn't exist""")
