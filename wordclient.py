import random
import sys
import socket

# How many bytes is the word length?
WORD_LEN_SIZE = 2

# Set RECV_SIZE to a random interger between 1 and 4096
RECV_SIZE = 1 # random.randint(1, 4096)

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

    word_packet = b''
    word = b''

    # TODO -- Write me!

    # copy word length and strip it
    # print('Looking for word_length in packet_buffer', end='')
    while len(packet_buffer) < WORD_LEN_SIZE:
        receive_word_packets(s)
        if len(packet_buffer) == 0:
            return None
    # print('')

    word_length = int.from_bytes(packet_buffer[:WORD_LEN_SIZE], 'big')
    # print("Word Length: " + str(word_length))
    packet_buffer = packet_buffer[WORD_LEN_SIZE:]
    # print('packet_buffer: ', end='')
    # print(packet_buffer)

    # copy word and strip it
    # print('Looking for word of length ' + str(word_length), end='')
    while len(packet_buffer) < word_length:
        receive_word_packets(s)
    # print('')

    word = packet_buffer[:word_length]
    # print('word: ' + str(word))
    packet_buffer = packet_buffer[word_length:]
    # print('packet_buffer: ', end='')
    # print(packet_buffer)

    # assemble word packet
    word_packet = int.to_bytes(WORD_LEN_SIZE, word_length, 'big') + word
    return word_packet


def receive_word_packets(s):
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

    # TODO -- Write me!

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
