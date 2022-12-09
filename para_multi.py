import threading

import paramiko
import subprocess
import os.path
import shlex

bws = [10, 20, 50, 100, 250, 500, 750, 1000]  # 8 bandwidths (Mbps)
rtts = [5, 10, 25, 50, 75, 100, 150, 200]  # 8 rtts (ms)
buffers = [100, 1000, 10000, 20000, 50000]  # 5 buffers (KBytes)
algos = ["bbr", "cubic"]
"""
    burst = 50MB should not be the bottleneck
    8 * 8 * 5 = 360 seconds total
    10 seconds/test = 1 hour for full suite
"""

# commands
# cmd = "iperf -c192.168.100.168 -t5 -b1g -e -Zbbr -yc -i1 -P2"
cmd3bbr = 'iperf3 -c 192.168.100.168 -p 5201 -t 10 -C bbr -J -P{0} --logfile {0}'
cmd3cubic = 'iperf3 -c 192.168.100.168 -p 5202 -t 10 -C cubic -J -P{0} --logfile {1}'
cmds = [cmd3bbr, cmd3cubic]

# setup
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("f1", username="root")


def setTC(link, tc_rtt, tc_bw, tc_buffer):
    netem_cmd = "sudo tc qdisc replace dev {0} root handle 1:0 netem delay {1}ms".format(link, tc_rtt / 2)
    netem_args = shlex.split(netem_cmd)  # list of args
    subprocess.run(netem_args)
    # subprocess.run(shlex.split("tc qdisc show dev vnet0"))

    tbf_cmd = "sudo tc qdisc replace dev {0} parent 1:1 handle 10: tbf rate {1}mbit limit {2}kb burst 50mb" \
        .format(link, tc_bw, tc_buffer)
    tbf_args = shlex.split(tbf_cmd)
    subprocess.run(tbf_args)
    # subprocess.run(shlex.split("tc qdisc show dev vnet1"))


# def runIperf(i_bw, i_rtt, i_buffer, i_algo, i_num_stream):
#     testName = "bw{0}rtt{1}buffer{2}_{3}".format(bw, rtt, buffer, algo)
#     # subprocess.run(shlex.split("tc qdisc show dev vnet1"))
#     stdin, stdout, stderr = ssh.exec_command(cmd3bbr.format(streams, testName))  # iperf3
#     stdin.close()  # do not remove
#
#     outlines = stdout.readlines()
#     errlines = stderr.readlines()
#     resp = ''.join(outlines + errlines)
#
#     fname = "results/bw{0}rtt{1}buffer{2}.json".format(bw, rtt, buffer)
#     finalname = os.path.join(os.getcwd(), fname)
#
#     # output
#     f = open(fname, 'w')
#     f.write("".join(resp))
#     f.close()

outlock = threading.Lock()

if __name__ == "__main__":
    threads = []

    # run suite
    for bw in bws:
        for rtt in rtts:
            for buffer in buffers:
                for algo, cmd in zip(algos, cmds):
                    # t = threading.Thread(target=)
                    setTC("vnet0", rtt, bw, buffer)
                    setTC("vnet1", rtt, bw, buffer)

                    testName = "results/bw{0}rtt{1}buffer{2}_{3}.json".format(bw, rtt, buffer, algo)
                    stdin, stdout, stderr = ssh.exec_command(cmd.format(3, testName))  # parallel connections, json name
                    stdin.close()  # do not remove

                    # need the file transfer to wait until test is done, preferably without wait()
                    ftp_client = ssh.open_sftp()
                    ftp_client.get(testName, testName)
                    ftp_client.close()

                    # outlines = stdout.readlines()
                    # errlines = stderr.readlines()
                    # resp = ''.join(outlines + errlines)
                    #
                    # fname = "results/" + testName
                    # # finalname = os.path.join(os.getcwd(), fname)
                    #
                    # # output
                    # f = open(fname, 'w')
                    # f.write("".join(resp))
                    # f.close()

    # cleanup
    ssh.close()

# subprocess.run(shlex.split("tc qdisc show dev vnet1"))
