import pexpect
import sys

local_pref = sys.argv[1]
# xterm r1
# Sur R1 pour set un local pref sur r3 
child = pexpect.spawn('telnet localhost 2605')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('access-list any permit 10.3.0.1/0')
child.sendline('route-map TEST permit 10')
child.sendline('match ip any')
child.sendline('set local-preference ' + local_pref)
child.kill(0)