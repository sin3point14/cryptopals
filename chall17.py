from chall11 import encrypt_aes_cbc,pkcs7_padding
from chall10 import decrypt_aes_cbc
from chall15 import validate_pkcs7
import os, random, base64
key = bytes(bytearray(os.urandom(16)))

strings = [b'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=', b'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=', b'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==', b'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==', b'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl', b'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==', b'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==', b'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=', b'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=', b'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93']
for i, s in enumerate(strings):
    strings[i] = base64.b64decode(s)
def generate():
    rand_plain = strings[random.randint(0,9)]
    padded_plain = pkcs7_padding(rand_plain,16)
    iv = bytes(bytearray(os.urandom(16)))
    cipher = encrypt_aes_cbc(padded_plain, key, iv)
    return iv + cipher
def oracle5(cipher, iv):
    return validate_pkcs7(decrypt_aes_cbc(cipher,key,iv))
    
def pwn_oracle5(cipher): # small error is that the first byte determined can be 0x1 of form a sequence of ... 0xn 0xn 0xn with padding bytes so it's a 50% chance for correct answer
    chunks, chunk_size = len(cipher), 16
    blocks = [ cipher[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
    plain = b''
    for i in reversed(range(1, len(blocks))):
        curr_block = blocks[i]
        prev_block = bytearray(blocks[i-1])
        curr_pwned = b''
        prev_block_orig = prev_block.copy()
        for curr_index in reversed(range(16)):
            x = 16-curr_index
            for b in range(15, curr_index, -1):
                prev_block[b] ^= (x) ^ (x-1)
            for a in range(256):
                prev_block[curr_index] = a
                if oracle5(bytes(prev_block) + curr_block, cipher[0:16]):
                    break
            curr_pwned = bytes([ x ^ prev_block[curr_index] ^ prev_block_orig[curr_index] ]) + curr_pwned
            print(curr_pwned)
        plain = curr_pwned + plain
    return plain
cipher = generate()
print(pwn_oracle5(cipher))