import pexpect

child = pexpect.spawn('telnet localhost 2605')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('access-list router3 permit 10.3.0.1/0')
child.sendline('route-map TEST permit 10')
child.sendline('match ip address router3')
child.sendline('set community 2:100')
child.kill(0)