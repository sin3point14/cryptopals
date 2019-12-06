import random

(w, n, m, r) = (32, 624, 397, 31)
a = 0x9908B0DF
(u, d) = (11, 0xFFFFFFFF)
(s, b) = (7, 0x9D2C5680)
(t, c) = (15, 0xEFC60000)
l = 18

f = 1812433253

MT = [0]*n
index = n+1
lower_mask = (1<<r) - 1
upper_mask = (((1<<w) - 1) ^ lower_mask)  # warning assuming r < w

def seed_mt(seed):
    global index
    index = n
    MT[0] = seed
    for i in range(1, n):
        MT[i] = ((1<<w)-1) & ( f * (MT[i-1] ^ (MT[i-1] >> (w-2))) + i )
def extract_number():
    global index
    if index >= n:
        if index > n:
            raise Exception('Generator was never seeded')
        twist()
    y = MT[index]
    y = y ^ ((y>>u) & d)
    y = y ^ ((y<<s) & b)
    y = y ^ ((y<<t) & c)
    y = y ^ (y>>l)

    index += 1
    return ((1<<w) - 1) & y
def twist():
    global index
    for i in range(n):
        x = (MT[i] & upper_mask) + (MT[(i+1)%n] & lower_mask)
        xA = x>>1
        if x % 2 != 0:
            xA ^= a
        MT[i] = MT[(i+m) % n] ^ xA
    index = 0
if __name__ == "__main__":
    seed_mt(1337)
    print(extract_number())