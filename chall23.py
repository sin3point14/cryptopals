import os
from chall21 import *
MT_Copy = []
numbers = []
seed = int.from_bytes( os.urandom(4), "little")
seed_mt(seed)
def rev_ls_and(y, s, b):
    orig = 0
    for i in range(w//s + 1):
        obtained = (y & ((1 << s) - 1))
        orig += (obtained << (i * s))
        b >>= s
        to_xor = (y & b) & ((1 << s) - 1)
        y >>= s
        y = y ^ to_xor
    return orig & ((1 << w) - 1)
def rev_bits(num,bitSize):
    binary = bin(num) 
    reverse = binary[-1:1:-1] 
    reverse = reverse + (bitSize - len(reverse))*'0'
    return int(reverse,2) 

def rev_rs_and(y, s, b):
    return rev_bits(rev_ls_and(rev_bits(y, w), s, rev_bits(b, w)), w)

for i in range(n):
    numbers += [extract_number()]

for i in numbers:
    i = rev_rs_and(i, l, (1<<w)-1)
    i = rev_ls_and(i, t, c)
    i = rev_ls_and(i, s, b)
    i = rev_rs_and(i, u, d)
    MT_Copy += [i]
print(MT_Copy == MT)