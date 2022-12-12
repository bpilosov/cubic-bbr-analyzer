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


def jsonToDataFrame(folder: str) -> pd.DataFrame:
    p = os.getcwd() + '/' + folder
    f_names = glob("*.json", root_dir=p)

    lst = []
    for f_name in sorted(f_names):
        params = str(f_name).split("_")
        bw = params[0][2:]
        rtt = params[1][3:]
        buffer = params[2][6:]
        algo = params[3].split(".")[0]
        f = json.load(open(p + '/' + f_name, 'r'))
        bytes_sent = f["end"]["sum_sent"]["bytes"]
        bytes_received = f["end"]["sum_received"]["bytes"]
        loss_rate = (bytes_sent - bytes_received) / bytes_sent
        time_elapsed = f["end"]["sum_sent"]["end"] - f["end"]["sum_sent"]["start"]
        goodput = f["end"]["sum_sent"]["bits_per_second"]
        retransmits = f["end"]["sum_sent"]["retransmits"]
        host_cpu = f["end"]["cpu_utilization_percent"]["host_total"]
        remote_cpu = f["end"]["cpu_utilization_percent"]["remote_total"]
        tmp = [bw, rtt, buffer, algo, bytes_sent, bytes_received, loss_rate, time_elapsed, goodput, retransmits,
               host_cpu, remote_cpu]
        tmp_df = pd.DataFrame(tmp).T
        lst.append(tmp_df)

    result = pd.concat(lst, ignore_index=True)
    result.columns = ["bandwidth", "delay", "buffer_size", "algorithm", "bytes_sent", "bytes_received", "loss_rate",
                      "time_elapsed", "goodput", "retransmits", "host_cpu", "remote_cpu"]
    # print(result)
    # result.to_csv(path_or_buf=folder + ".csv")
    return result


def avgThreeResults(test_name: str):
    df = pd.read_csv("zips/" + test_name + ".csv")
    df1 = pd.read_csv("zips/" + test_name + ".csv")
    df2 = pd.read_csv("zips/" + test_name + ".csv")
    col_algo = df["algorithm"]

    lst = [df, df1, df2]
    df_concat = pd.concat(lst)
    # print(df_concat)
    # df_concat.to_csv(path_or_buf="concat" + ".csv")

    by_row_index = df_concat.groupby(df_concat.index)
    df_means = by_row_index.mean()
    df_means.insert(4, "algorithm", col_algo)
    # print(df_means)
    df_means.to_csv(path_or_buf="means" + ".csv")


def analyzeFairness(df: pd.DataFrame, test_name: str):
    bbrRows = df.iloc[::2]
    cubicRows = df.iloc[1::2]
    lstb = []
    lstc = []
    for b, c in zip(bbrRows.iterrows(), cubicRows.iterrows()):
        bdata = b[1]
        cdata = c[1]
        tot_goodput = bdata["goodput"] + cdata["goodput"]
        b_ratio = bdata["goodput"] / tot_goodput
        c_ratio = cdata["goodput"] / tot_goodput
        # print(b[0])
        # print(b_ratio)
        # tmp_b = pd.DataFrame([b[0], b_ratio])
        tmp_b = pd.DataFrame([b_ratio], index=[b[0]])
        # print(tmp_b)
        tmp_c = pd.DataFrame([c_ratio], index=[c[0]])
        lstb.append(tmp_b)
        lstc.append(tmp_c)

    bcol = pd.concat(lstb)
    ccol = pd.concat(lstc)
    bcol.columns = ["bbr_ratio"]
    ccol.columns = ["cubic_ratio"]

    df = df.join([bcol, ccol])

    # df_sorted = df.sort_values(by=['bbr_ratio', 'cubic_ratio'], ascending=[False, False])
    bbr_advantage = df.query("bbr_ratio >= 0.6")
    cubic_advantage = df.query("cubic_ratio >= 0.6")
    sorted_bbr_advantage = bbr_advantage.sort_values(by=["bbr_ratio"], ascending=False)
    sorted_cubic_advantage = cubic_advantage.sort_values(by=["cubic_ratio"], ascending=False)

    print(sorted_bbr_advantage)
    print(sorted_cubic_advantage)
    sorted_bbr_advantage.to_csv(path_or_buf="sorted_bbr_advantage" + test_name + ".csv")
    sorted_cubic_advantage.to_csv(path_or_buf="sorted_cubic_advantage" + test_name + ".csv")


if __name__ == "__main__":
    test = "60sec640tests2"
    analyzeFairness(jsonToDataFrame(test), test)
