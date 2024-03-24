alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"

encrypt_args = {
    'input': ['any']
}

decrypt_args = {
    'input': ['any']
}

def encrypt(input_bytes):
    encoded_data = bytearray()
    bits = 0
    bits_count = 0

    for byte in input_bytes:
        bits <<= 8
        bits += byte
        bits_count += 8

        while bits_count >= 5:
            index = (bits >> (bits_count - 5)) & 31
            encoded_data.append(ord(alphabet[index]))
            bits_count -= 5
            bits &= (1 << bits_count) - 1

    if bits_count > 0:
        bits <<= 5 - bits_count
        index = bits & 31
        encoded_data.append(ord(alphabet[index]))

    while len(encoded_data) % 8 != 0:
        encoded_data.append(ord("="))

    return bytes(encoded_data)

def decrypt(input_bytes):
    decoded_data = bytearray()
    bits = 0
    bits_count = 0

    for byte in input_bytes:
        if byte == ord("="):
            break

        index = alphabet.index(chr(byte))
        bits <<= 5
        bits += index
        bits_count += 5

        while bits_count >= 8:
            decoded_data.append((bits >> (bits_count - 8)) & 255)
            bits_count -= 8
            bits &= (1 << bits_count) - 1

    return bytes(decoded_data)