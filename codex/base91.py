# WE NEED A DECODE FUNCTION
BASE91_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~\""

def encode(input_string):
    output = []
    data = input_string.encode('utf-8')
    value = 0
    n = 0
    bits = 0

    for byte in data:
        value |= byte << bits
        bits += 8
        if bits >= 13:
            curr_value = value & 8191
            output.append(BASE91_ALPHABET[curr_value % 91])
            output.append(BASE91_ALPHABET[curr_value // 91])
            value >>= 13
            bits -= 13

    while bits > 0:
        output.append(BASE91_ALPHABET[value % 91])
        value //= 91
        bits -= 13

    return ''.join(output)
