import socket as so
import time

host_name = 'time.nist.gov'
host_port = 37

host_address = (host_name, host_port)


def system_seconds_since_1900():
    # The time-server returns the number of seconds since 1900, but Unix
    # systems return the number of seconds since 1970. This function
    # computes the number of seconds since 1900 on the system.

    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(time.time())
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch


def try_and_get_time():
    # create socket
    socket = so.socket()

    # connect to time.nist.gov:37
    socket.connect(host_address)

    # receive data (4 bytes)
    p = socket.recv(4)

    socket.close()
    return p


package = try_and_get_time()

# decode with .from_bytes()
server_time = int.from_bytes(package, 'big')

# print the value
print('NIST time\t: ' + str(server_time))

# print system time
system_time = system_seconds_since_1900()
print('System time\t: ' + str(system_time))
