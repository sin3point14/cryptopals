from chall21 import *
import os, random
seed = int.from_bytes( os.urandom(2), "little")
def mt_stream(plain, seed):
    seed_mt(seed)
    out = b''
    for i in plain:
        out += bytes([i ^ (extract_number() & 0xff)])
    return out
def pwn_mt_stream(cipher, known):
    for i in range (0xffff+1):
        if mt_stream(cipher, i)[-len(known):] == known:
            return i
prefix = os.urandom(random.randint(1, 10))
known = b'A'*14
print(pwn_mt_stream(mt_stream(prefix + known, seed), known) == seed)