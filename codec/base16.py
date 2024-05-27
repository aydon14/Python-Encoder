encrypt_args = {
    'input': None,
    'IE': True
}

decrypt_args = {
    'input': None,
    'IE': True
}

def encrypt(input_bytes):
    output = bytearray()
    for byte in input_bytes:
        output += "{:02X}".format(byte).encode('utf-8')
    return bytes(output)

def decrypt(input_bytes):
    output = bytearray()
    input_string = input_bytes.upper().decode('utf-8')
    for i in range(0, len(input_string), 2):
        output.append(int(input_string[i:i+2], 16))
    return bytes(output)