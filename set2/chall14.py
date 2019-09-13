from chall12 import *
prefix = bytes(bytearray(os.urandom(random.randrange(0,1024))))
def oracle3(plain):
    return oracle2(prefix + plain)
def pwn_oracle3():
    x = count_aes_ecb_repetitions(oracle3(b""), 16)
    test = b"A"*32 #block_size * 2
    while True:
        if count_aes_ecb_repetitions(oracle3(test), 16) > x:
            break
        test += b"A"
    repetition = oracle3(test)
    for pos in range(0, len(repetition)-16, 16):
        if repetition[pos:pos+16] == repetition[pos+16:pos+32]:
            break
    padding = b"A"*(len(test)-32)
    block_no=0
    block_size = 16
    plaintext = b""
    for _ in range(len(secert)//block_size+1):
        for i in range(block_size):
            test = b"A"*(block_size-i-1)
            oracle_says = oracle3(padding+test)
            oracle_says = oracle_says[pos:]
            for j in range(128):
                cmp1 = oracle3(padding+test+plaintext+bytes([j]))[pos:]
                cmp2 = oracle_says[block_no*block_size:block_no*block_size+block_size]
                cmp1 = cmp1[block_no*block_size:block_no*block_size+block_size]
                if cmp1 == cmp2:
                    plaintext += bytes([j])
                    break
        block_no += 1
    return plaintext
if __name__ == "__main__":
    print(pwn_oracle3())