# Binary

encrypt_args = {
    'input': ['any']
}

decrypt_args = {
    'input': ['any']
}

def encrypt(input_bytes):
    result = ""
    
    for byte in input_bytes:
        result += bin(byte)[2:].zfill(8)

    return result.encode('utf-8')

def decrypt(input_bytes):
    result = bytearray()
    
    for i in range(0, len(input_bytes), 8):
        result.append(int(input_bytes[i:i+8], 2))

    return bytes(result)