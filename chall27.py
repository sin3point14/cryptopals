from chall11 import encrypt_aes_cbc,pkcs7_padding
from chall10 import decrypt_aes_cbc
import os

key = iv = os.urandom(16)

def oracle27_1(plain):
    return encrypt_aes_cbc(plain, key, iv)
def oracle27_2(cipher):
    plain = decrypt_aes_cbc(cipher, key, iv)
    for i in plain:
        if i > 127:
            return plain
    return b""
plain = b"A"*16 + b"B"*16 + b"C"*16
cipher = oracle27_1(plain)
cipher_mod = cipher[:16] + b"\x00"*16 + cipher[:16]
plain_mod = oracle27_2(cipher_mod)
if cipher_mod == b"":
    print("failed")
    exit(0)
key2 = b"".join([bytes([i^j]) for i,j in zip(plain_mod[:16], plain_mod[-16:])])
print(key2)
print(key)
if(key == key2):
    print("pwned")