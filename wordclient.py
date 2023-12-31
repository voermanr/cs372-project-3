import random
import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2

# Set RECV_SIZE to a random integer between 1 and 4096
RECV_SIZE = random.randint(1, 4096)


def usage():
    print("usage: wordclient.py server port", file=sys.stderr)


packet_buffer = b''


def get_next_word_packet(s):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """

    global packet_buffer

    # load more data if the buffer isn't big enough for the word_length
    while len(packet_buffer) < WORD_LEN_SIZE:
        if not stuff_buffer(s):
            return None

    else:
        # copy word length from buffer
        word_length = int.from_bytes(packet_buffer[:WORD_LEN_SIZE], 'big')

        # calc the word packet length
        word_packet_length = word_length + WORD_LEN_SIZE

        # load more data if the packet_buffer is shorter than the word packet
        while len(packet_buffer) < word_packet_length:
            stuff_buffer(s)

        # slice off the word packet
        word_packet = packet_buffer[:word_packet_length]
        packet_buffer = packet_buffer[word_packet_length:]

        return word_packet


def stuff_buffer(s):
    """
    receives `RECV_SIZE` bytes from the server, and appends it to the global `packet_buffer`.
    Returns True if data was added to the packet_buffer. Otherwise, returns false
    :param s: socket connected to word server
    """

    global packet_buffer

    r = s.recv(RECV_SIZE)
    if len(r) != 0:
        packet_buffer += r
        return True

    else:
        return False


def extract_word(word_packet):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """

    return word_packet[WORD_LEN_SIZE:].decode()

# Do not modify:

def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1

    s = socket.socket()
    s.connect((host, port))

    print("Getting words:")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)

        print(f"    {word}")

    s.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
