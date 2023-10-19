# There's a time and the time is now and it's right for me
# It's right for me, and the time is now
# There's a word and the word is love and it's right for me
# It's right for me, and the word is love

import socket as so
import time

host_name = 'time.nist.gov'
host_port = 37

host_address = (host_name, host_port)
server_time = 0


def delay_connection(seconds_to_delay: int, verbose: bool = True):
    print('Waiting ' + str(seconds_to_delay) + ' seconds', end= '')
    for cycle in range(seconds_to_delay):
        if verbose:
            print('.', end='')
        time.sleep(1)


def system_seconds_since_1900():
    # The time-server returns the number of seconds since 1900, but Unix
    # systems return the number of seconds since 1970. This function
    # computes the number of seconds since 1900 on the system.

    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(time.time())
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch


# create socket
socket = so.socket()

# connect to time.nist.gov:37
delay_connection(4)
socket.connect(host_address)
print('Connected')

# reveive data (4 bytes)
package = socket.recv(4)
print('Package from ' + str(host_name) + ':' + str(host_port) + ' => ' + str(package))
if package == b'':
    print('Who packed this?')
socket.close()

# decode with .from_bytes()
server_time = int.from_bytes(package, 'big')

# print the value
print('NIST time\t: ' + str(server_time))

# print system time
system_time = system_seconds_since_1900()
print('System time\t: ' + str(system_time))

# evaluate results
delta_time = abs(system_time - server_time)
if delta_time <= 10:
    print('Great!')
elif delta_time <= 86400:
    print('OK.')
elif delta_time <= 1000000:
    print('Not good.')
else:
    print('Broked')