import pexpect
import sys
# xterm r1
# Sur R1 pour set un local pref sur r3 

community = sys.argv[1]
route_map = sys.argv[2]
sequence = sys.argv[3]
child = pexpect.spawn('telnet localhost 2605')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('route-map {} permit {}'.format(route_map,sequence))
child.sendline('match community {}'.format(community))
child.sendline('set as-path prepend 1 1')
child.sendline('on-match next')
child.sendline('exit')
child.kill(0)