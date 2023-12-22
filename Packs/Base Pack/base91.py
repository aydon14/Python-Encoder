# These functions are inspired by Adrien Beraud
# https://github.com/aberaud/base91-python

base91_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~"'

def decode(input):
    table = {char: index for index, char in enumerate(base91_alphabet)}
    value, buffer, bits_count, output = -1, 0, 0, bytearray()

    for char in input:
        character = table[char]
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

    return bytes(output).decode("utf-8")

def encode(input):
    utf_input = input.encode("utf-8")
    buffer, bits_count, output = 0, 0, []

    for byte in utf_input:
        buffer |= byte << bits_count
        bits_count += 8
        while bits_count >= 13:
            value = buffer & 8191
            shift = 13 if value > 88 else 14
            buffer, bits_count = (buffer >> shift, 
                                  bits_count - shift)
            output.extend(map(ord, [base91_alphabet[value % 91], 
                                    base91_alphabet[value // 91]]))

    if bits_count:
        output.extend(map(ord, [base91_alphabet[buffer % 91]]
                          + ([base91_alphabet[buffer // 91]] 
                             if bits_count > 7 or buffer > 90 else [])))

    return ''.join(map(chr, output))
