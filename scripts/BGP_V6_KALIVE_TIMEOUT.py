import pexpect
import sys
#getting into config
args = sys.argv
NEIGHBORSV6 = args[1]
size = len(NEIGHBORSV6)
KALIVE = args[2]
TIMEOUT = args[3]
print(args[1])
print(args[2])
print(args[3])

BGP_FRROUTING = pexpect.spawn('telnet localhost 2605')
BGP_FRROUTING.expect('Password:')
BGP_FRROUTING.sendline('zebra')
BGP_FRROUTING.sendline('enable')
BGP_FRROUTING.sendline('configure terminal')
BGP_FRROUTING.sendline('router bgp')
BGP_FRROUTING.sendline('neighbor ' + NEIGHBORSV6 + 'timers ' + KALIVE + ' ' + TIMEOUT)
BGP_FRROUTING.kill(0)