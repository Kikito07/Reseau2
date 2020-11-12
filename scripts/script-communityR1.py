#!/usr/bin/env python3
import pexpect
# xterm r1
# Sur R1 pour set un local pref sur r3 
child = pexpect.spawn('telnet localhost 2605')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('bgp community-list standard comm3 permit 2:100')
child.sendline('route-map r1 permit 10')
child.sendline('match community comm3')
child.sendline('set local-preference 300')
child.kill(0)