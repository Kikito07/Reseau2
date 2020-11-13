import pexpect
import sys
# xterm r1
# Sur R1 pour set un local pref sur r3 
child = pexpect.spawn('telnet localhost 2605')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('bgp community-list standard AS_PREPEND permit 2:100')
child.sendline('route-map AS_PREPEND permit 10')
child.sendline('match community AS_PREPEND')
child.sendline('set as-path prepend 1')
child.kill(0)