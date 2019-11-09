from Crypto.Cipher import AES
from chall10 import decrypt_aes_cbc
import os
import base64
import random

def count_aes_ecb_repetitions(ciphertext, block):
    chunks = [ciphertext[i:i + block] for i in range(0, len(ciphertext), block)]
    number_of_duplicates = len(chunks) - len(set(chunks))
    return number_of_duplicates

def encrypt_aes_ecb(plain, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(plain)
def encrypt_aes_cbc(plain, key, iv):
    block = len(iv)
    cipher = b""
    decipher = AES.new(key, AES.MODE_ECB)
    xor = iv
    for i in range(0, len(plain), block):
        temp = bytes([b1 ^ b2 for b1, b2 in zip(plain[i:i+block], xor)])
        cipher += decipher.encrypt(temp)
        xor = cipher[-1*block:]
    return cipher

def pkcs7_padding(text, block):
    if len(text) % block == 0:
        pad = block
    else:
        pad = block - len(text) % block
    padded = text + bytes([pad])*pad
    return padded
def oracle(plain):
    key = bytes(bytearray(os.urandom(16)))
    prefix = bytes(bytearray(os.urandom(random.randrange(5,11))))
    suffix = bytes(bytearray(os.urandom(random.randrange(5,11))))
    newplain = pkcs7_padding(prefix + plain + suffix, 16)
    if random.randrange(0, 2) == 1:
        print("~CBC")
        return encrypt_aes_cbc(newplain, key, bytes(bytearray(os.urandom(16))))
    else:
        print("~ECB")
        return encrypt_aes_ecb(newplain, key)
def detect_cipher(cipher):
    if count_aes_ecb_repetitions(cipher, 16) > 0:
        return "ECB"
    else:
        return "CBC"
if __name__ == "__main__":
    for _ in range(10):
        enc = oracle(bytes([0]*64))
        print(detect_cipher(enc))
