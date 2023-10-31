def encode(data):
    base32_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    encoded_data = ""
    bits = 0
    bits_count = 0

    for char in data:
        bits <<= 8
        bits += ord(char)
        bits_count += 8

        while bits_count >= 5:
            index = (bits >> (bits_count - 5)) & 31
            encoded_data += base32_alphabet[index]
            bits_count -= 5
            bits &= (1 << bits_count) - 1

    if bits_count > 0:
        bits <<= 5 - bits_count
        index = bits & 31
        encoded_data += base32_alphabet[index]

    # Add padding to make the length a multiple of 8
    while len(encoded_data) % 8 != 0:
        encoded_data += "="

    return encoded_data

def decode(encoded_data):
    base32_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    decoded_data = ""
    bits = 0
    bits_count = 0

    for char in encoded_data:
        if char == "=":
            break

        index = base32_alphabet.index(char)
        bits <<= 5
        bits += index
        bits_count += 5

        while bits_count >= 8:
            byte = (bits >> (bits_count - 8)) & 255
            decoded_data += chr(byte)
            bits_count -= 8
            bits &= (1 << bits_count) - 1

    return decoded_data
