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

    # copy word length
    while len(packet_buffer) < WORD_LEN_SIZE:
        stuff_buffer(s)
        if len(packet_buffer) == 0:
            return None
    # print('')

    word_length = int.from_bytes(packet_buffer[:WORD_LEN_SIZE], 'big')
    word_length_offset = word_length + WORD_LEN_SIZE
    # print("Word Length: " + str(word_length))
    # packet_buffer = packet_buffer[WORD_LEN_SIZE:]
    # print('packet_buffer: ', end='')
    # print(packet_buffer)

    # copy word_packet
    # print('Looking for word of length ' + str(word_length), end='')
    while len(packet_buffer) < word_length_offset:
        stuff_buffer(s)
    # print('')

    word_packet = packet_buffer[:word_length_offset]
    # print('word_packet: ' + str(word_packet) + '\t' + 'len: ' + str(int.from_bytes(word_packet[:WORD_LEN_SIZE], 'big')) + '\tword: ' + str(word_packet[WORD_LEN_SIZE:]))
    packet_buffer = packet_buffer[word_length_offset:]
    # print('packet_buffer: ', end='')
    # print(packet_buffer)

    # assemble word packet
    # word_packet = int.to_bytes(WORD_LEN_SIZE, word_length, 'big') + word
    return word_packet


def stuff_buffer(s):
    """
    receives `RECV_SIZE` bytes from the server, and appends it to the global `packet_buffer`
    :param s: socket connected to word server
    """
    global packet_buffer

    r = s.recv(RECV_SIZE)
    if len(r) == 0:
        return

    # print('.', end='')
    packet_buffer += r


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
