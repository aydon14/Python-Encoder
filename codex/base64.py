base64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def encode(input_text):
    output_text = ""
    bits = 0
    bits_count = 0

    for char in input_text:
        bits <<= 8
        bits += ord(char)
        bits_count += 8

        while bits_count >= 6:
            index = (bits >> (bits_count - 6)) & 63
            output_text += base64_alphabet[index]
            bits_count -= 6
            bits &= (1 << bits_count) - 1

    if bits_count > 0:
        bits <<= 6 - bits_count
        index = bits & 63
        output_text += base64_alphabet[index]

    # Add padding to make the length a multiple of 4
    while len(output_text) % 4 != 0:
        output_text += "="

    return output_text

def decode(input_text):
    output_text = ""
    bits = 0
    bits_count = 0

    for char in input_text:
        if char == "=":
            break

        index = base64_alphabet.index(char)
        bits <<= 6
        bits += index
        bits_count += 6

        while bits_count >= 8:
            byte = (bits >> (bits_count - 8)) & 255
            output_text += chr(byte)
            bits_count -= 8
            bits &= (1 << bits_count) - 1

    return output_text
