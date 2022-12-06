import iperf3
import netimpair

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client = iperf3.Client()
    client.duration = 10
    client.server_hostname = '192.168.100.168'
    client.port = 5201
    # client.congestion_control = "bbr"
    client.json_output = True

    print('Connecting to {0}:{1}'.format(client.server_hostname, client.port))
    result = client.run()

    if result.error:
        print(result.error)
    print(result)
