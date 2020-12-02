import sys
import pexpect


community = sys.argv[1]
rm = sys.argv[2]
seq = sys.argv[3]

# xterm r1
# Sur R1 pour set un local pref sur r3 
child = pexpect.spawn('telnet localhost 2605')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('route-map {} deny {}'.format(rm, seq))
child.sendline('match community {}'.format(community))
child.sendline('exit')
child.kill(0)