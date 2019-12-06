import time, random
from chall21 import *

def stupid_random_number():
    r = random.randint(40, 1000)
    time.sleep(r)
    t = int(time.time())
    seed_mt(t+r)
    print(t+r)
    time.sleep(random.randint(40, 1000))
    return extract_number()
def pwn_stupid_random_number(pwn_this):
    t = int(time.time())
    while True:
        print(t)
        seed_mt(t)
        if extract_number() == pwn_this:
            return t
        t-=1
print(pwn_stupid_random_number(stupid_random_number()))