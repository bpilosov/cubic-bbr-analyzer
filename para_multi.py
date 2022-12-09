import shlex
import subprocess
import threading
from time import sleep
import paramiko

bws = [10, 20, 50, 100, 250, 500, 750, 1000]  # 8 bandwidths (Mbps)
rtts = [5, 10, 25, 50, 75, 100, 150, 200]  # 8 rtts (ms)
buffers = [100, 1000, 10000, 20000, 50000]  # 5 buffers (KBytes)
algos = ["cubic", "bbr"]
ports = [5201, 5202]

"""
    http://ce.sc.edu/cyberinfra/workshops/Material/NTP/Lab%205.pdf 
    page 10: burst = bw/1000. 10mb = 10kb, 1000mb = 1000kb
    8 * 8 * 5 = 360 seconds total
    10 seconds/test = 1 hour for full suite
"""

# commands
# cmd = "iperf -c192.168.100.168 -t5 -b1g -e -Zbbr -yc -i1 -P2"
cmd3 = 'iperf3 -c 192.168.100.168 -p {3} -t 10 -C {2} -J -P{0} --logfile {1}'


# cmd3bbr = 'iperf3 -c 192.168.100.168 -p 5201 -t 10 -C {2} -J -P{0} --logfile {1}'
# cmd3cubic = 'iperf3 -c 192.168.100.168 -p 5202 -t 10 -C {2} -J -P{0} --logfile {1}'
# cmds = [cmd3bbr, cmd3cubic]


def setTC(link, tc_rtt, tc_bw, tc_buffer):
    netem_cmd = "sudo tc qdisc replace dev {0} root handle 1:0 netem delay {1}ms".format(link, tc_rtt / 2)
    netem_args = shlex.split(netem_cmd)  # list of args
    subprocess.run(netem_args)
    # subprocess.run(shlex.split("tc qdisc show dev vnet0"))

    tbf_cmd = "sudo tc qdisc replace dev {0} parent 1:1 handle 10: tbf rate {1}mbit limit {2}kb burst {3}kb" \
        .format(link, tc_bw, tc_buffer, tc_bw)
    tbf_args = shlex.split(tbf_cmd)
    subprocess.run(tbf_args)
    # subprocess.run(shlex.split("tc qdisc show dev vnet1"))


def runIperf(i_bw, i_rtt, i_buffer, i_algo, i_num_stream, i_port):
    # setup
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("f1", username="root")
    ftp_client = ssh.open_sftp()

    test_name = "results/bw{0}rtt{1}buffer{2}_{3}.json".format(i_bw, i_rtt, i_buffer, i_algo)
    try:
        ftp_client.remove(test_name)  # remove previous results if present
    except IOError:
        pass  # not present

    # parallel connections, json name, TCP algo, port number
    stdin, stdout, stderr = ssh.exec_command(cmd3.format(i_num_stream, test_name, i_algo, i_port))
    stdin.close()  # do not remove

    stdout.channel.recv_exit_status()  # blocking until iperf is complete

    # # need the file transfer to wait until test is done, preferably without wait()
    ftp_client.get(test_name, test_name)  # transfer file to local
    ftp_client.close()
    ssh.close()


def zero():
    sleep(10)
    return 0


if __name__ == "__main__":
    threads = []
    # run suite
    for bw in bws:
        for rtt in rtts:
            for buffer in buffers:
                setTC("vnet0", rtt, bw, buffer)
                setTC("vnet1", rtt, bw, buffer)

                for algo, port in zip(algos, ports):
                    t = threading.Thread(target=runIperf, args=(bw, rtt, buffer, algo, 1, port))
                    # t = threading.Thread(target=zero)
                    threads.append(t)
                    t.start()
                while len(threads):
                    y = threads[0]
                    y.join()
                    threads.remove(y)

# subprocess.run(shlex.split("tc qdisc show dev vnet1"))
