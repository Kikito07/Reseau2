import pexpect
import sys
import time
#getting into config
args = sys.argv
NEIGHBORSV6 = args[1]
KALIVE = args[2]
TIMEOUT = args[3]
BGP_FRROUTING = pexpect.spawn('telnet localhost 2605')
BGP_FRROUTING.expect('Password:')
BGP_FRROUTING.sendline('zebra')
BGP_FRROUTING.sendline('enable')
BGP_FRROUTING.sendline('configure terminal')
BGP_FRROUTING.sendline('router bgp')
BGP_FRROUTING.sendline('neighbor ' + NEIGHBORSV6 + ' timers ' + KALIVE + ' ' + TIMEOUT)
BGP_FRROUTING.sendline('exit')
BGP_FRROUTING.sendline('write memory')
BGP_FRROUTING.sendline('neighbor {} shutdown'.format(NEIGHBORSV6))
time.sleep(3)
BGP_FRROUTING.sendline('no neighbor {} shutdown'.format(NEIGHBORSV6))
BGP_FRROUTING.kill(0)


