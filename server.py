import iperf3


server = iperf3.Server()
server.verbose = True

print('Running server: {0}:{1}'.format(server.bind_address, server.port))

while True:
    result = server.run()

    if result.error:
        print(result.error)
