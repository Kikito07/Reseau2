import sys
import pexpect


neighbor = sys.argv[1]
# xterm r1
# Sur R1 pour set un local pref sur r3 
child = pexpect.spawn('telnet localhost 2605')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('route-map {} deny {}'.format('server', 10))
child.sendline('exit')
child.sendline('router bgp')
child.sendline('address-family ipv6 unicast')
child.sendline('neighbor {} route-map {} {}'.format(neighbor, 'server', 'out'))
child.sendline('')
child.sen
child.kill(0)