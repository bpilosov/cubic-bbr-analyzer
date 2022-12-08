import subprocess

import paramiko

# commands
cmd = "iperf -c192.168.100.168 -t5 -b1g -e -Zbbr -yc -i1 -P2"
cmd3 = 'iperf3 -V -c 192.168.100.168 -t 2 -C bbr'

# setup
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("f1", username="root")
stdin, stdout, stderr = ssh.exec_command(cmd)
stdin.close()  # do not remove

# output
outlines = stdout.readlines()
errlines = stderr.readlines()
resp = ''.join(outlines + errlines)
f = open("ptest.csv", 'w')
f.write("".join(resp))

# cleanup
f.close()
ssh.close()
