import pexpect
child = pexpect.spawn('telnet localhost 2604')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('interface PAR1-eth0')
child.sendline('ip ospf cost 50')
child.kill(0)