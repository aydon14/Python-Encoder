# Decimal

encrypt_args = {
    'input': ['any']
}

decrypt_args = {
    'input': ['any']
}

def encrypt(input):
    plaintext_int = 0
    for byte in input:
        plaintext_int = plaintext_int * 256 + byte
    ciphertext_str = str(plaintext_int)
    return ciphertext_str.encode('utf-8')

def decrypt(input_bytes):
    ciphertext_str = input_bytes.decode('utf-8')
    plaintext_int = int(ciphertext_str)
    plaintext_bytes = bytearray()
    while plaintext_int > 0:
        plaintext_bytes.append(plaintext_int % 256)
        plaintext_int //= 256
    return bytes(reversed(plaintext_bytes))