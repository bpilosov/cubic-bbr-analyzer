import iperf3
import netimpair

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client = iperf3.Client()
    client.duration = 60
    client.server_hostname = '192.168.101.210'
    client.port = 5201

    print('Connecting to {0}:{1}'.format(client.server_hostname, client.port))
    result = client.run()

    if result.error:
        print(result.error)
