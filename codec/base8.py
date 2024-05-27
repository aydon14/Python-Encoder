# Octal

encrypt_args = {
    'input': None,
    'IE': True
}

decrypt_args = {
    'input': None,
    'IE': True
}

def encrypt(input_bytes):
    result = ""

    for byte in input_bytes:
        result += oct(byte)[2:].zfill(3)

    return result.encode('utf-8')

def decrypt(input_bytes):
    result = bytearray()

    for i in range(0, len(input_bytes), 3):
        result.append(int(input_bytes[i:i+3], 8))

    return bytes(result)