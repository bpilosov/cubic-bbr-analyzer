import matplotlib.pyplot as plt
import pandas as pd
import json
from glob import glob
import os

bws = [10, 20, 50, 100, 250, 500, 750, 1000]  # 8 bandwidths (Mbps)
rtts = [5, 10, 25, 50, 75, 100, 150, 200]  # 8 rtts (ms)
buffers = [100, 1000, 10000, 20000, 50000]  # 5 buffers (KBytes)
algos = ["bbr", "cubic"]
basestring = "bw{0}rtt{1}buffer{2}_{3}.json"


def sortedToDataFrame(folder):
    lst = []
    for x in bws:
        for y in rtts:
            for z in buffers:
                for bc in algos:
                    f_name = basestring.format(x, y, z, bc)
                    f = json.load(open('10sec640testsBadFileNames/' + f_name, 'r'))
                    bytes_sent = f["end"]["sum_sent"]["bytes"]
                    time_elapsed = f["end"]["sum_sent"]["end"] - f["end"]["sum_sent"]["start"]
                    goodput = f["end"]["sum_sent"]["bits_per_second"]
                    retransmits = f["end"]["sum_sent"]["retransmits"]
                    host_cpu = f["end"]["cpu_utilization_percent"]["host_total"]
                    remote_cpu = f["end"]["cpu_utilization_percent"]["remote_total"]
                    tmp = [x, y, z, bc, bytes_sent, time_elapsed, goodput, retransmits, host_cpu, remote_cpu]
                    tmp_df = pd.DataFrame(tmp).T
                    lst.append(tmp_df)

    result = pd.concat(lst, ignore_index=True)
    result.columns = ["bandwidth", "delay", "buffer_size", "algorithm", "bytes_sent", "time_elapsed", "goodput",
                      "retransmits", "host_cpu", "remote_cpu"]
    print(result)
    result.to_csv(path_or_buf=folder + ".csv")
    return result


def jsonToDataFrame(folder):
    p = os.getcwd() + '/' + folder
    f_names = glob("*.json", root_dir=p)

    lst = []
    for f_name in f_names:
        params = str(f_name).split("_")
        bw = params[0][2:]
        rtt = params[1][3:]
        buffer = params[2][6:]
        algo = params[3].split(".")[0]
        f = json.load(open('10sec640tests/' + f_name, 'r'))
        bytes_sent = f["end"]["sum_sent"]["bytes"]
        time_elapsed = f["end"]["sum_sent"]["end"] - f["end"]["sum_sent"]["start"]
        goodput = f["end"]["sum_sent"]["bits_per_second"]
        retransmits = f["end"]["sum_sent"]["retransmits"]
        host_cpu = f["end"]["cpu_utilization_percent"]["host_total"]
        remote_cpu = f["end"]["cpu_utilization_percent"]["remote_total"]
        tmp = [bw, rtt, buffer, algo, bytes_sent, time_elapsed, goodput, retransmits, host_cpu, remote_cpu]
        tmp_df = pd.DataFrame(tmp).T
        lst.append(tmp_df)

    result = pd.concat(lst, ignore_index=True)
    result.columns = ["bandwidth", "delay", "buffer_size", "algorithm", "bytes_sent", "time_elapsed", "goodput",
                      "retransmits", "host_cpu", "remote_cpu"]
    print(result)
    result.to_csv(path_or_buf=folder + ".csv")
    return result


if __name__ == "__main__":
    # sortedToDataFrame("10sec640testsBadFileNames")
    jsonToDataFrame("60sec27tests")
