import pexpect
import sys
#getting into config
args = sys.argv
NEIGHBORSV6 = args[1]
size = len(NEIGHBORSV6)
TTLS = args[2]
PASSWORDS = args[3]


BGP_FRROUTING = pexpect.spawn('telnet localhost 2605')
BGP_FRROUTING.expect('Password:')
BGP_FRROUTING.sendline('zebra')
BGP_FRROUTING.sendline('enable')
BGP_FRROUTING.sendline('configure terminal')
BGP_FRROUTING.sendline('router bgp')
for i in range(0,size):
    BGP_FRROUTING.sendline('neighbor ' + NEIGHBORSV6[i] + 'ttl-security hops ' + TTLS[i])
    BGP_FRROUTING.sendline('neighbor ' + NEIGHBORSV6[i] + 'password ' + PASSWORDS[i])
#configuring