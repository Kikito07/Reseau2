import pexpect
import sys

password = sys.argv[1]
interface = sys.argv[2]

child = pexpect.spawn('telnet localhost 2604')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('interface ' + interface)
child.sendline("ip ospf authentication-key " + password)
child.sendline('exit')
child.sendline('router ospf')
child.sendline('area 0 authentication')
child.sendline('')
child.kill(0)