import pexpect
import sys
import time
fileName = sys.argv[1]
# xterm r1
# Sur R1 pour set un local pref sur r3 

child = pexpect.spawn('tshark -w output.pcap -F pcap')
child.sendline('')

