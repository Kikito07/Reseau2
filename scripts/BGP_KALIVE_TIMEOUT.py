import pexpect
import sys
#getting into config
args = sys.argv
KALIVE = args[1]
TIMEOUT = args[2]
BGP_FRROUTING = pexpect.spawn('telnet localhost 2605')
BGP_FRROUTING.expect('Password:')
BGP_FRROUTING.sendline('zebra')
BGP_FRROUTING.sendline('enable')
BGP_FRROUTING.sendline('configure terminal')
BGP_FRROUTING.sendline('router bgp')
BGP_FRROUTING.sendline('timers ' + 'bgp ' + KALIVE + ' ' + TIMEOUT)
BGP_FRROUTING.kill(0)
