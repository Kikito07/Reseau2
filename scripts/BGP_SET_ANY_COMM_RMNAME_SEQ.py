import pexpect
import sys
community = sys.argv[1]
name = sys.argv[2]
sequence = sys.argv[3]
# xterm r1
# Sur R1 pour set un local pref sur r3 
child = pexpect.spawn('telnet localhost 2605')
child.expect('Password:')
child.sendline('zebra')
child.sendline('enable')
child.sendline('configure terminal')
child.sendline('ipv6 access-list any permit ::/0')
child.sendline('route-map {} permit {}'.format(name,sequence))
child.sendline('match ipv6 address any')
child.sendline('set community {} additive'.format(community))
child.sendline('on-match next')
child.sendline('write memory')
child.kill(0)