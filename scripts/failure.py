import pexpect
child = pexpect.spawn('ip link set dev eth0 down')
child.kill(0)