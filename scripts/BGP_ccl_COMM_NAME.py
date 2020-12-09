import pexpect
import sys

community = sys.argv[1]
name = sys.argv[2]

# xterm r1
# Sur R1 pour set un local pref sur r3 
child = pexpect.spawn('telnet localhost 2605')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('bgp community-list standard {} permit {}'.format(name,community))
child.sendline('exit')
child.kill(0)

