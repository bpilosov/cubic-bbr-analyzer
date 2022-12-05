import getpass
import subprocess
import shlex
import paramiko

if __name__ == '__main__':
    # f0pass = getpass.getpass("f0 password:")
    # f1pass = getpass.getpass("f1 password:")

    # must have already set up ssh keys with guests
    cmd = "ssh root@f1 'python3 client.py'"
    cmd = shlex.split(cmd)
    subprocess.run(cmd)


