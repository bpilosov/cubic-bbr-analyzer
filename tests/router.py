import csv
import getpass
import subprocess
import shlex
import paramiko

if __name__ == '__main__':
    # f0pass = getpass.getpass("f0 password:")
    # f1pass = getpass.getpass("f1 password:")

    server_cmd = "ssh root@f0 'python3 ~/cubic-bbr-analyzer/server.py'"
    server_cmd = shlex.split(server_cmd)

    subprocess.Popen(server_cmd, stdin=None, stdout=None, stderr=None, close_fds=True)

    # must have already set up ssh keys with guests
    # f1 is client
    client_cmd = "ssh root@f1 'python3 ~/cubic-bbr-analyzer/client.py'"
    client_cmd = shlex.split(client_cmd)

    f = open("../test.json", 'w')
    subprocess.run(client_cmd, stdout=f)

