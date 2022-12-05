import getpass
import subprocess
import shlex
import paramiko

if __name__ == '__main__':
    # f0pass = getpass.getpass("f0 password:")
    # f1pass = getpass.getpass("f1 password:")

    f0_cmd = "ssh root@f0 'python3 ~/cubic-bbr-analyzer/server.py'"
    f0_cmd = shlex.split(f0_cmd)

    subprocess.run(f0_cmd)

    # must have already set up ssh keys with guests
    # f1 is client
    f1_cmd = "ssh root@f1 'python3 ~/cubic-bbr-analyzer/client.py'"
    f1_cmd = shlex.split(f1_cmd)

    subprocess.run(f1_cmd)
