import pexpect
import sys
import time
#getting into config
args = sys.argv
NEIGHBORSV6 = args[1]
KALIVE = args[2]
TIMEOUT = args[3]
child = pexpect.spawn('telnet localhost 2605')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('router bgp')
child.sendline('no neighbor ' + NEIGHBORSV6 + ' ebgp-multihop')
child.sendline('neighbor ' + NEIGHBORSV6 + ' timers ' + KALIVE + ' ' + TIMEOUT)
child.sendline('exit')
child.kill(0)


