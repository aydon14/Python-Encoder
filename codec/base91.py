# These functions are inspired by Adrien Beraud
# https://github.com/aberaud/base91-python

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~"'

encrypt_args = {
    'input': ['any']
}

decrypt_args = {
    'input': ['any']
}

def decrypt(input_bytes):
    table = {char: index for index, char in enumerate(alphabet)}
    value, buffer, bits_count, output = -1, 0, 0, bytearray()

    for byte in input_bytes:
        character = table[chr(byte)]
        if value < 0:
            value = character
        else:
            value += character * 91
            buffer |= value << bits_count
            bits_count += 13 if (value & 8191) > 88 else 14
            while bits_count > 7:
                output.append(buffer & 255)
                buffer >>= 8
                bits_count -= 8
            value = -1

    if value + 1:
        output.append((buffer | value << bits_count) & 255)

    return bytes(output)

def encrypt(input_bytes):
    buffer, bits_count, output = 0, 0, []

    for byte in input_bytes:
        buffer |= byte << bits_count
        bits_count += 8
        while bits_count >= 13:
            value = buffer & 8191
            shift = 13 if value > 88 else 14
            buffer, bits_count = (buffer >> shift, 
                                  bits_count - shift)
            output.extend(map(ord, [alphabet[value % 91], 
                                    alphabet[value // 91]]))

    if bits_count:
        output.extend(map(ord, [alphabet[buffer % 91]]
                          + ([alphabet[buffer // 91]] 
                             if bits_count > 7 or buffer > 90 else [])))

    return bytes(output)