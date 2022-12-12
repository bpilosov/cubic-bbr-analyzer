# BBR-Cubic Flow Analyzer
# para_multi.py - 
SSH to a machine, run Iperf3 tests aimed at your server, return the json output over sftp.

Preconditions: A client you can ssh into, a server that you have running iperf3 in server mode.
Must make a directory on client and host for the tests with matching name.

# jsonToCsv -
Functions for turning jsons into dataframes and export as csv

Turn json into pandas dataframe 

Average three json results together

Construct the ratio of bbr/cubic throughput from a json

# decisionTree.py
Copied from https://github.com/DavyCao/Dumbbell-Testbed/commit/6306b82c52987a755ec30e61bc05c1f228116b79

Used in https://www3.cs.stonybrook.edu/~arunab/papers/imc19_bbr.pdf