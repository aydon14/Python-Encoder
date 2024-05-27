# Made by Aydon Fauscett

S_BOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
]

RCON = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f
]

def key_expansion(key, Nr):
    key_size = len(key)
    key_words = [key[i:i + 4] for i in range(0, len(key), 4)]
    expanded_keys = list(key_words)
    Nk = key_size // 4

    for i in range(Nk, 4 * (Nr + 1)):
        temp = expanded_keys[i - 1]
        if key_size == 32 and i % Nk == 4:
            temp = [S_BOX[b] for b in temp]
        elif i % Nk == 0:
            temp = [temp[1], temp[2], temp[3], temp[0]]

            for j in range(4):
                temp[j] = S_BOX[temp[j]]

            temp[0] ^= RCON[i // Nk - 1]

        expanded_keys.append([a ^ b for a, b in zip(expanded_keys[i - Nk], temp)])

    return expanded_keys

def sub_bytes(state):
    return [[S_BOX[b] for b in row] for row in state]

def shift_rows(state, inv=False):
    for i in range(4):
        shift = -i if inv else i
        state[0][i], state[1][i], state[2][i], state[3][i] = (
            state[(0 + shift) % 4][i],
            state[(1 + shift) % 4][i],
            state[(2 + shift) % 4][i],
            state[(3 + shift) % 4][i],
        )
    
    return state

def mix_columns(state):
    for i in range(4):
        s = [state[i][j] for j in range(4)]

        state[i][0] = mul(0x02, s[0]) ^ mul(0x03, s[1]) ^ s[2] ^ s[3]
        state[i][1] = s[0] ^ mul(0x02, s[1]) ^ mul(0x03, s[2]) ^ s[3]
        state[i][2] = s[0] ^ s[1] ^ mul(0x02, s[2]) ^ mul(0x03, s[3])
        state[i][3] = mul(0x03, s[0]) ^ s[1] ^ s[2] ^ mul(0x02, s[3])

    return state

def mul(a, b):
    p = 0
    
    for _ in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        a &= 0xFF
        if hi_bit_set:
            a ^= 0x1b
        b >>= 1
        
    return p

def add_round_key(state, round_key):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]

    return state

def encrypt_block(block, key, Nr):
    state = block[:]
    state = add_round_key(state, key[:4])

    for round in range(1, Nr):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, key[4 * round: 4 * round + 4])
    
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, key[4 * Nr: 4 * Nr + 4])

    return bytes(sum(state, []))

def ecb_encrypt(plaintext, key):
    Nr = 0
    if len(key) == 16:
        Nr = 10
    elif len(key) == 24:
        Nr = 12
    elif len(key) == 32:
        Nr = 14
    expanded_key = key_expansion(key, Nr)
    ciphertext = b''
    blocks = [plaintext[i:i+block_size] for i in range(0, len(plaintext), block_size)]

    for block in blocks:

        state = [list(block[i:i+4]) for i in range(0, len(block), 4)]
        encrypted_block = encrypt_block(state, expanded_key, Nr)
        ciphertext += encrypted_block

    return ciphertext

def inc32(counter_block):
    counter = int.from_bytes(counter_block, 'big')
    counter += 1
    return counter.to_bytes(16, 'big')

def gctr(icb, X, key):
    n = ((len(X) + 15) // 16) + 1
    if len(X) % 16 != 0:
        n = n - 1
    blocks = [X[i:i+block_size] for i in range(0, len(X), block_size)]

    CB = icb
    Y = b''

    for i in range(1, n):
        CB = inc32(CB)
        encrypted_block = ecb_encrypt(CB, key)
        Y += bytes(a ^ b for a, b in zip(encrypted_block, blocks[i-1]))

    last_block = blocks[-1]
    msb_len_x_n = len(last_block) % block_size
    CB_last = inc32(CB)
    encrypted_last_block = ecb_encrypt(CB_last, key)[:msb_len_x_n]
    Y += bytes(a ^ b for a, b in zip(encrypted_last_block, last_block))

    return Y

def gf128_mul(x, y):
    y = int.from_bytes(y, 'big')

    z = 0
    for i in range(127, -1, -1):
        z ^= x * ((y >> i) & 1)
        x = (x >> 1) ^ ((x & 1) * 0xE1000000000000000000000000000000)

    return z

def ghash(H, A, C):
    input_data = A
    if len(A) % 16 != 0:
        input_data += b'\x00' * (16 - len(A) % 16)
    input_data += C
    if len(C) % 16 != 0:
        input_data += b'\x00' * (16 - len(C) % 16)
    
    input_data += (len(A) * 8).to_bytes(8, 'big') + (len(C) * 8).to_bytes(8, 'big')
    Y = 0
    blocks = [input_data[i:i + block_size] for i in range(0, len(input_data), block_size)]

    for block in blocks:
        X_i = int.from_bytes(block, byteorder='big')
        Y ^= X_i
        Y = gf128_mul(Y, H)

    return Y.to_bytes(16, byteorder='big')

encrypt_args = {
    'input': None,
    'key': [16, 24, 32],
    'iv': [16],
    'ad': None,
    'IE': False
}

decrypt_args = {
    'input': None,
    'key': [16, 24, 32],
    'iv': [16],
    'ad': None,
    'tag': [32],
    'IE': False
}

block_size = 16

def encrypt(plaintext, key, iv, ad):
    key = key.encode('utf-8')
    iv = iv.encode('utf-8')
    ad = ad.encode('utf-8')
    H = ecb_encrypt(b"\x00" * 16, key)
    if len(iv) == 12:
        J_0 = iv + b"\x00\x00\x00\x01"
    else:
        J_0 = ghash(H, b'', iv)

    ciphertext = gctr(J_0, plaintext, key)
    tag = (bytes(a ^ b for a, b in zip(ghash(H, ad, ciphertext), ecb_encrypt(J_0, key)))).hex()
    
    return ciphertext, tag

def decrypt(ciphertext, key, iv, ad, tag):
    key = key.encode('utf-8')
    iv = iv.encode('utf-8')
    ad = ad.encode('utf-8')
    tag = bytes.fromhex(tag)
    H = ecb_encrypt(b"\x00" * 16, key)
    if len(iv) == 12:
        J_0 = iv + b"\x00\x00\x00\x01"
    else:
        J_0 = ghash(H, b'', iv)

    decrypted_tag = bytes(a ^ b for a, b in zip(ghash(H, ad, ciphertext), ecb_encrypt(J_0, key)))

    plaintext = gctr(J_0, ciphertext, key)
    
    if decrypted_tag != tag:
        warning = "Tag authentication failed. Data may be corrupt or tampered with."
        return plaintext, warning

    return plaintext