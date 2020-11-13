#!/usr/bin/env python3
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
child.sendline('bgp community-list standard COMM_TEST permit 2:100')
child.sendline('route-map TEST permit 10')
child.sendline('match community COMM_TEST')
child.sendline('set local-preference ' + local_pref)
child.kill(0)