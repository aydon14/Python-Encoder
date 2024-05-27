alphabet = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstu"

encrypt_args = {
    'input': None,
}

decrypt_args = {
    'input': None,
}

def encrypt(input_bytes):
    result = bytearray()
    input_len = len(input_bytes)

    i = 0
    while i < input_len:
        chunk = input_bytes[i:i+4]
        i += 4

        value = 0
        for j, byte in enumerate(chunk):
            value |= byte << (8 * (3 - j))

        encoded = bytearray()
        for _ in range(5):
            encoded.insert(0, alphabet[value % 85])
            value //= 85

        result += encoded

    if input_len % 4 != 0:
        result = result[:-(4 - input_len % 4)]

    return bytes(result)

def decrypt(input_bytes):
    result = bytearray()
    input_len = len(input_bytes)

    i = 0
    while i < input_len:
        chunk = input_bytes[i:i+5]
        i += 5

        value = 0
        for j, char in enumerate(chunk):
            if char == ord('u'):
                char = ord('!')
            index = alphabet.index(char)
            value = value * 85 + index

        decoded = bytearray()
        for _ in range(4):
            decoded.insert(0, (value & 0xFF))
            value >>= 8

        result += decoded

    if input_len % 5 != 0:
        result = result[:-(5 - input_len % 5)]

    if result[-1] == 0x00:
        result[-1] = ord('!')

    return bytes(result)