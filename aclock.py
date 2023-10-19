# There's a time and the time is now and it's right for me
# It's right for me, and the time is now
# There's a word and the word is love and it's right for me
# It's right for me, and the word is love

import socket as so
import time

host_name = 'time.nist.gov'
host_port = 37

host_address = (host_name, host_port)


def delay_connection(seconds_to_delay: int, verbose: bool = True):
    print('Waiting ' + str(seconds_to_delay) + ' seconds', end= '')
    for cycle in range(seconds_to_delay):
        if verbose:
            print('.', end='')
        time.sleep(1)


# create socket
socket = so.socket()

# connect to time.nist.gov:37
delay_connection(4)
socket.connect(host_address)
print('Connected')

# reveive data (4 bytes)
package = socket.recv(4)
print('Package from ' + str(host_name) + ':' + str(host_port) + ' => ' + str(package))
socket.close()

# decode with .from_bytes()

# print the value

# print system time
