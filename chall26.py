from chall18 import aes_ctr
from chall16 import check_admin
import os

key = bytes(bytearray(os.urandom(16)))

def oracle26(a):
    b=b"comment1=cooking%20MCs;userdata="+a.replace(b';',b'').replace(b'=',b'')+b";comment2=%20like%20a%20pound%20of%20bacon"
    return aes_ctr(b, key, 0)
def pwn_oracle26(target):
    payload= b"A"*(len(target)+1)
    print(payload)
    out = oracle26(payload)
    print(out)
    pre = len("comment1=cooking%20MCs;userdata=")
    post = len(";comment2=%20like%20a%20pound%20of%20bacon")
    new = out[:pre+1]
    print(new)
    for i in range(len(target)):
        new += bytes([out[pre+1+i] ^ ord('A') ^ target[i]])
    return new + out[-post:]
print(aes_ctr(pwn_oracle26(b";admin=true"), key, 0))