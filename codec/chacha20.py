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
    
encrypt_args = {
    'key': [32],
    'counter': None,
    'iv': [12],
    'input': None,
    'IE': True
}

encrypt_args = {
    'key': [32],
    'counter': None,
    'iv': [12],
    'input': None,
    'IE': True
}

def encrypt(key, counter, iv, plaintext):
    key = key.encode('utf-8')
    counter = int(counter)
    iv = iv.encode('utf-8')
    encrypted = bytearray()
    block_size = 64
    for i in range(0, len(plaintext), block_size):
        block = chacha20_block(key, counter, iv)
        encrypted += bytes(p ^ b for p, b in zip(plaintext[i:i+block_size], block))
        counter += 1
    return bytes(encrypted)

def decrypt(key, counter, iv, plaintext):
    return encrypt(key, counter, iv, plaintext)