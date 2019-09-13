from Crypto.Cipher import AES
from chall11 import *
import os
import base64
import random

key = bytes(bytearray(os.urandom(16)))
secert = base64.b64decode(b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
def oracle2(plain):
    newplain = pkcs7_padding(plain + secert, 16)
    return encrypt_aes_ecb(newplain, key)
def find_block_size_ecb():
    for i in range(1, 129):
        test = (b"A")*2*i
        ret = oracle2(test)
        if ret[0:i] == ret[i:2*i]:
            return i
    return -1
def pwn_oracle2(block_size):
    block_no=0
    plaintext = b""
    for _ in range(len(secert)//block_size+1):
        for i in range(block_size):
            test = b"A"*(block_size-i-1)
            oracle_says = oracle2(test)
            for j in range(128):
                if oracle2(test+plaintext+bytes([j]))[block_no*block_size:block_no*block_size+block_size] == oracle_says[block_no*block_size:block_no*block_size+block_size]:
                    plaintext += bytes([j])
                    break
        block_no += 1
    return plaintext

if __name__ == "__main__":
    block_size = find_block_size_ecb()
    print("block size -> " + str(block_size))
    print("pwned -> " + str(pwn_oracle2(block_size)))
