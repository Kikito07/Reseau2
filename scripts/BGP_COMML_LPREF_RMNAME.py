import pexpect
import sys

community = sys.argv[1]
local_pref = sys.argv[2]
route_map = sys.argv[3]
# xterm r1
# Sur R1 pour set un local pref sur r3 
child = pexpect.spawn('telnet localhost 2605')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('route-map {} permit 10'.format(route_map))
child.sendline('match community {}'.format(community))
child.sendline('set local-preference {}'.format(local_pref))
child.sendline('write memory')
child.sendline('exit')
child.kill(0)