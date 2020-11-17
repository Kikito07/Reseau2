import pexpect
import sys
#getting into config
args = sys.argv
NEIGHBORSV6 = args[1]
TTL = args[2]
PASSWORD = args[3]

BGP_FRROUTING = pexpect.spawn('telnet localhost 2605')
BGP_FRROUTING.expect('Password:')
BGP_FRROUTING.sendline('zebra')
BGP_FRROUTING.sendline('enable')
BGP_FRROUTING.sendline('configure terminal')
BGP_FRROUTING.sendline('router bgp')
BGP_FRROUTING.sendline('no neighbor ' + NEIGHBORSV6 + ' ebgp-multihop')
BGP_FRROUTING.sendline('neighbor ' + NEIGHBORSV6 + ' ttl-security hops ' + TTL)
BGP_FRROUTING.sendline('neighbor ' + NEIGHBORSV6 + ' password ' + PASSWORD)
BGP_FRROUTING.kill(0)
