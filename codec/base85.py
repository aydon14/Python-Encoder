# ascii85 with modified alphabet as defined in RFC 1924 (IPv6)
# https://www.dcode.fr/ascii-85-encoding

alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~"

encrypt_args = {
    'input': None,
    'IE': True
}

decrypt_args = {
    'input': None,
    'IE': True
}

def encrypt(input_bytes):
    result = bytearray()
    data_len = len(input_bytes)

    i = 0
    while i < data_len:
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

    if data_len % 4 != 0:
        result = result[:-(4 - data_len % 4)]

    return bytes(result)

def decrypt(encoded_input):
    data_len = len(encoded_input)
    result = bytearray()

    i = 0
    while i < data_len:
        chunk = encoded_input[i:i+5]
        i += 5

        if b'u' in chunk:
            chunk = chunk.replace(b'u', b'!')

        value = 0
        for j, char in enumerate(chunk):
            index = alphabet.index(chr(char))
            value = value * 85 + index

        decoded = bytearray()
        for _ in range(4):
            decoded.insert(0, (value & 0xFF))
            value >>= 8

        result += decoded

    if data_len % 5 != 0:
        result = result[:-(5 - data_len % 5)]

    if result and result[-1] == 0x00:
        result[-1] = ord('!')

    return bytes(result)