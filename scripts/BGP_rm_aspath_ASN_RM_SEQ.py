import pexpect
import sys
#getting into config
args = sys.argv
ASN = args[1]
route_map = args[2]
sequence = args[3]

child = pexpect.spawn('telnet localhost 2605')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('route-map {} permit {}'.format(route_map, sequence))
child.sendline('set as-path exclude {}'.format(ASN))
child.sendline('exit')
child.kill(0)
