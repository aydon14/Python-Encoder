alphabet = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstu"

def encode(input):
    data = input.encode('utf-8')
    result = ""
    data_len = len(data)

    i = 0
    while i < data_len:
        chunk = data[i:i+4]
        i += 4

        value = 0
        for j, byte in enumerate(chunk):
            value |= byte << (8 * (3 - j))

        encoded = ""
        for _ in range(5):
            encoded = alphabet[value % 85] + encoded
            value //= 85

        result += encoded

    # Remove padding if data length is not a multiple of 4
    if data_len % 4 != 0:
        result = result[:-(4 - data_len % 4)]

    return result

def decode(data):
    result = bytearray()
    data_len = len(data)

    i = 0
    while i < data_len:
        chunk = data[i:i+5]
        i += 5

        value = 0
        for j, char in enumerate(chunk):
            if char == 'u':
                char = '!'
            index = alphabet.index(char)
            value = value * 85 + index

        decoded = bytearray()
        for _ in range(4):
            decoded.insert(0, (value & 0xFF))
            value >>= 8

        result += decoded

    # Remove padding if data length is not a multiple of 5
    if data_len % 5 != 0:
        result = result[:-(5 - data_len % 5)]

    # Replace the last byte if it's 0x00 with '!'
    if result[-1] == 0x00:
        result[-1] = ord('!')

    return result.decode('utf-8')
