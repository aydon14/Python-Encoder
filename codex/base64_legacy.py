""" This is the original C/C++ (written in python) version
      of base64. Refer to base64.py for the python code.   """

base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def encode(input):
    encoded = ""
    i = 0
    j = 0
    char_array_3 = [0] * 3
    char_array_4 = [0] * 4

    for character in input:
        char_array_3[i] = ord(character)
        i += 1

        if i == 3:
            char_array_4[0] = (char_array_3[0] & 0xFC) >> 2
            char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xF0) >> 4)
            char_array_4[2] = ((char_array_3[1] & 0x0F) << 2) + ((char_array_3[2] & 0xC0) >> 6)
            char_array_4[3] = char_array_3[2] & 0x3F

            for i in range(4):
                encoded += base64_chars[char_array_4[i]]

            i = 0

    if i > 0:
        for j in range(i, 3):
            char_array_3[j] = 0

        char_array_4[0] = (char_array_3[0] & 0xFC) >> 2
        char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xF0) >> 4)
        char_array_4[2] = ((char_array_3[1] & 0x0F) << 2) + ((char_array_3[2] & 0xC0) >> 6)

        for j in range(i + 1):
            encoded += base64_chars[char_array_4[j]]

        while i < 3:
            encoded += '='
            i += 1

    return encoded


def decode(input):
    decoded = ""
    i = 0
    j = 0
    char_array_4 = [0] * 4
    char_array_3 = [0] * 3

    for character in input:
        if character == '=':
            break
        if character == '\n' or character == '\r':
            continue

        char_array_4[i] = base64_chars.find(character)
        i += 1

        if i == 4:
            char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4)
            char_array_3[1] = ((char_array_4[1] & 0x0F) << 4) + ((char_array_4[2] & 0x3C) >> 2)
            char_array_3[2] = ((char_array_4[2] & 0x03) << 6) + char_array_4[3]

            for i in range(3):
                decoded += chr(char_array_3[i])

            i = 0

    if i > 0:
        for j in range(i, 4):
            char_array_4[j] = 0

        char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4)
        char_array_3[1] = ((char_array_4[1] & 0x0F) << 4) + ((char_array_4[2] & 0x3C) >> 2)
        char_array_3[2] = ((char_array_4[2] & 0x03) << 6) + char_array_4[3]

        for j in range(i - 1):
            decoded += chr(char_array_3[j])

    return decoded
