import iperf3
import netimpair

delays = [0, 1, 5, 10, 25, 50, 75, 100, 150, 200]
bws = [1, 10, 100, 1000, 10000]
limits = [1000, 2000, 5000, 10000, 500000, 1000000, 2000000, 5000000, 10000000, 100000000]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client = iperf3.Client()
    client.duration = 1
    client.server_hostname = '192.168.100.168'
    # client.server_hostname = '127.0.0.0' # for testing local
    client.port = 5201
    client.verbose = True
    client.json_output = True

    result = client.run()
    if result.error:
        print(result.error)
    # f = open("test.json", 'w')
    # f.write(result.text)
    # f.close()
    print(result)

    del client

    client = iperf3.Client()
    client.duration = 1
    client.server_hostname = '192.168.100.168'
    # client.server_hostname = '127.0.0.0' # for testing local
    client.port = 5201
    client.verbose = True
    client.json_output = True
    result = client.run()
    if result.error:
        print(result.error)
    # f0 = open("test0.json", 'w')
    # f0.write(result.text)
    # f0.close()
    print(result)


