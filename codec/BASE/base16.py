def encode(input):
    output = ""
    for char in input:
        output += "{:02X}".format(ord(char))
    return output

def decode(input):
    output = ""
    input = input.upper()  # Ensure uppercase characters for consistency
    for i in range(0, len(input), 2):
        output += chr(int(input[i:i+2], 16))
    return output