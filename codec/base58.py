alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

encrypt_args = {
    'input': None,
    'IE': True
}

decrypt_args = {
    'input': None,
    'IE': True
}

def encrypt(input_bytes):
    output_text = bytearray()
    bits = 0
    bits_count = 0

    for byte in input_bytes:
        bits <<= 8
        bits += byte
        bits_count += 8

        while bits_count >= 5:
            index = (bits >> (bits_count - 5)) & 31
            output_text.append(ord(alphabet[index]))
            bits_count -= 5
            bits &= (1 << bits_count) - 1

    if bits_count > 0:
        bits <<= 5 - bits_count
        index = bits & 31
        output_text.append(ord(alphabet[index]))

    return bytes(output_text)

def decrypt(input_bytes):
    output_text = bytearray()
    bits = 0
    bits_count = 0

    for byte in input_bytes:
        if byte not in alphabet.encode('utf-8'):
            break

        index = alphabet.index(chr(byte))
        bits <<= 5
        bits += index
        bits_count += 5

        while bits_count >= 8:
            output_text.append((bits >> (bits_count - 8)) & 255)
            bits_count -= 8
            bits &= (1 << bits_count) - 1

    return bytes(output_text)