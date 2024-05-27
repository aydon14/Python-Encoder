def rotate(v, c):
    return (v << c) & 0xffffffff | (v >> (32 - c))

def quarter_round(x, a, b, c, d):
    x[a] = (x[a] + x[b]) & 0xffffffff
    x[d] = rotate(x[d] ^ x[a], 16)
    
    x[c] = (x[c] + x[d]) & 0xffffffff
    x[b] = rotate(x[b] ^ x[c], 12)
    
    x[a] = (x[a] + x[b]) & 0xffffffff
    x[d] = rotate(x[d] ^ x[a], 8)
    
    x[c] = (x[c] + x[d]) & 0xffffffff
    x[b] = rotate(x[b] ^ x[c], 7)

def chacha20_block(key, counter, iv):
    constants = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
    
    key_st = [int.from_bytes(key[i:i+4], 'little') for i in range(0, len(key), 4)]
    iv_st = [int.from_bytes(iv[i:i+4], 'little') for i in range(0, len(iv), 4)]
    
    state = constants + key_st + [counter] + iv_st
    working_state = list(state)
    
    for _ in range(10):
        quarter_round(working_state, 0, 4, 8, 12)
        quarter_round(working_state, 1, 5, 9, 13)
        quarter_round(working_state, 2, 6, 10, 14)
        quarter_round(working_state, 3, 7, 11, 15)
        quarter_round(working_state, 0, 5, 10, 15)
        quarter_round(working_state, 1, 6, 11, 12)
        quarter_round(working_state, 2, 7, 8, 13)
        quarter_round(working_state, 3, 4, 9, 14)

    return b''.join(((working_state[i] + state[i]) & 0xffffffff)
                    .to_bytes(4, 'little') for i in range(16))

def chacha_encrypt(key, counter, iv, plaintext):
    encrypted = bytearray()
    block_size = 64
    for i in range(0, len(plaintext), block_size):
        block = chacha20_block(key, counter, iv)
        encrypted += bytes(p ^ b for p, b in zip(plaintext[i:i+block_size], block))
        counter += 1
    return bytes(encrypted)

def poly1305_key_gen(key, iv):
    return chacha20_block(key, 0, iv)[:32]

def clamp_r(r):
    r[3] &= 15
    r[7] &= 15
    r[11] &= 15
    r[15] &= 15
    r[4] &= 252
    r[8] &= 252
    r[12] &= 252

def poly1305_mac(key, msg):
    r = list(key[:16])
    clamp_r(r)
    s = int.from_bytes(key[16:], byteorder='little')

    p = (1 << 130) - 5
    acc = 0

    for i in range(0, len(msg), 16):
        n = int.from_bytes(msg[i:i+16] + b'\x01', byteorder='little')
        acc = (acc + n) * int.from_bytes(bytes(r), byteorder='little') % p

    acc = (acc + s) % (1 << 128)
    return acc.to_bytes(16, byteorder='little')

def pad16(data):
    if len(data) % 16 != 0:
        return data + b'\x00' * (16 - len(data) % 16)
    return data

encrypt_args = {
    'key': [32],
    'iv': [12],
    'input': None,
    'aad': None,
    'IE': False
}

decrypt_args = {
    'key': [32],
    'iv': [12],
    'input': None,
    'aad': None,
    'tag': [32],
    'IE': False
}

def encrypt(key, iv, plaintext, aad):
    key = key.encode('utf-8')
    aad = aad.encode('utf-8')
    iv = iv.encode('utf-8')
    counter = 1
    
    ciphertext = chacha_encrypt(key, counter, iv, plaintext)
    
    poly_key = poly1305_key_gen(key, iv)

    aad_len = len(aad).to_bytes(8, 'little')
    ciphertext_len = len(ciphertext).to_bytes(8, 'little')
    mac_data = pad16(aad) + pad16(ciphertext) + aad_len + ciphertext_len
    
    tag = poly1305_mac(poly_key, mac_data).hex()
    
    return ciphertext, tag

def decrypt(key, iv, ciphertext, aad, tag):
    key = key.encode('utf-8')
    aad = aad.encode('utf-8')
    iv = iv.encode('utf-8')
    tag = bytes.fromhex(tag)
    counter = 1
    poly_key = poly1305_key_gen(key, iv)

    aad_len = len(aad).to_bytes(8, 'little')
    ciphertext_len = len(ciphertext).to_bytes(8, 'little')
    mac_data = pad16(aad) + pad16(ciphertext) + aad_len + ciphertext_len
    plaintext = chacha_encrypt(key, counter, iv, ciphertext)
    
    if poly1305_mac(poly_key, mac_data) != tag:
        warning = "Tag authentication failed. Data may be corrupt or tampered with."
        return plaintext, warning
    
    return plaintext