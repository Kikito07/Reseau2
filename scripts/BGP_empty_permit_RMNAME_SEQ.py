import pexpect
import sys
route_map = sys.argv[1]
sequence = sys.argv[2]

# xterm r1
# Sur R1 pour set un local pref sur r3 
child = pexpect.spawn('telnet localhost 2605')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('route-map {} permit {}'.format(route_map,sequence))
child.sendline('exit')
child.kill(0)