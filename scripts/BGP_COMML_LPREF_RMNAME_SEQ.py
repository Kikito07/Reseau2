import pexpect
import sys

community = sys.argv[1]
local_pref = sys.argv[2]
route_map = sys.argv[3]
sequence = sys.argv[4]
# xterm r1
# Sur R1 pour set un local pref sur r3 
child = pexpect.spawn('telnet localhost 2605')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('route-map {} permit {}'.format(route_map, sequence))
child.sendline('match community {}'.format(community))
child.sendline('set local-preference {}'.format(local_pref))
child.sendline('on-match next')
child.sendline('exit')
child.kill(0)