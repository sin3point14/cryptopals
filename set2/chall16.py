from chall11 import pkcs7_padding, encrypt_aes_cbc
from chall10 import decrypt_aes_cbc
import os
key = bytes(bytearray(os.urandom(16)))
iv = bytes(bytearray(os.urandom(16)))
def oracle4(a):
    b=b"comment1=cooking%20MCs;userdata="+a.replace(b';',b'').replace(b'=',b'')+b";comment2=%20like%20a%20pound%20of%20bacon"
    return encrypt_aes_cbc(pkcs7_padding(b, 16), key, iv)
def check_admin(a):
    return decrypt_aes_cbc(a, key, iv).find(b';admin=true;') != -1
def pwn_oracle4():
    reqd = b";admin=true;"+bytes([1])*4
    target = b";comment2=%20lik"
    payload = b"A"*16
    enc = bytearray(oracle4(payload))
    new = b""
    for i in range(len(reqd)):
        enc[i+32] = reqd[i]^target[i]^enc[i+32]
    print(check_admin(bytes(enc)))
if __name__ == "__main__":
    print(check_admin(oracle4(b"lol;pwned=1")))
    pwn_oracle4()