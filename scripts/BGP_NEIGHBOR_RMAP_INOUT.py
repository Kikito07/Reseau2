import pexpect
import sys
import time

neighbor = sys.argv[1]
route_map = sys.argv[2]
in_out = sys.argv[3]
# xterm r1
# Sur R1 pour set un local pref sur r3 
child = pexpect.spawn('telnet localhost 2605')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('router bgp')
child.sendline('address-family ipv6 unicast')
child.sendline('neighbor {} route-map {} {}'.format(neighbor, route_map, in_out))
child.sendline('exit')
child.sendline('write-memory')
child.sendline('neighbor {} shutdown'.format(neighbor))
time.sleep(3)
child.sendline('no neighbor {} shutdown'.format(neighbor))
child.kill(0)