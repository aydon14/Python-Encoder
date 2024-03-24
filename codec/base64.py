alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

encrypt_args = {
    'input': ['any']
}

decrypt_args = {
    'input': ['any']
}

def encrypt(input_bytes):
    output_text = bytearray()
    bits = 0
    bits_count = 0

    for byte in input_bytes:
        bits <<= 8
        bits += byte
        bits_count += 8

        while bits_count >= 6:
            index = (bits >> (bits_count - 6)) & 63
            output_text.append(ord(alphabet[index]))
            bits_count -= 6
            bits &= (1 << bits_count) - 1

    if bits_count > 0:
        bits <<= 6 - bits_count
        index = bits & 63
        output_text.append(ord(alphabet[index]))

    while len(output_text) % 4 != 0:
        output_text.append(ord("="))

    return bytes(output_text)

def decrypt(input_bytes):
    output_text = bytearray()
    bits = 0
    bits_count = 0

    for byte in input_bytes:
        if byte == ord("="):
            break

        index = alphabet.index(chr(byte))
        bits <<= 6
        bits += index
        bits_count += 6

        while bits_count >= 8:
            output_text.append((bits >> (bits_count - 8)) & 255)
            bits_count -= 8
            bits &= (1 << bits_count) - 1

    return bytes(output_text)