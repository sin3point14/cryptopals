import struct, binascii
from chall28 import mod_wrap, leftrotate

def F(x,y,z):
    return (x & y) | (~x & z)
def G(x,y,z):
    return (x & y) | (x & z) | (y & z)
def H(x,y,z):
    return x ^ y ^ z

def round1(a, b, c, d, k, s):
    return leftrotate(mod_wrap(a + F(b,c,d) + k), s)
def round2(a, b, c, d, k, s):
    return leftrotate(mod_wrap(a + G(b,c,d) + k + 0x5A827999), s)
def round3(a, b, c, d, k, s):
    return leftrotate(mod_wrap(a + H(b,c,d) + k + 0x6ED9EBA1), s)

X = []

def md_pad(plain):
    bitlength = len(plain) * 8
    plain += b"\x80"
    end = (bitlength + 1) % 512
    if end > 448:
        add = (512-end+448)
        plain += b"\x00"*(add//8)
    else:
        add = (448-end) 
        plain += b"\x00"*(add//8)
    plain += struct.pack("<Q", bitlength)
    return plain


def md4(plain):
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    plain = md_pad(plain)

    blocks = [plain[0+i:64+i] for i in range(0, len(plain), 64)]
    for block in blocks:
        words = [int.from_bytes(block[0+i:4+i], "little") for i in range(0, len(block), 4)]
        global X
        X = []
        for j in range(16) :
            X.append(words[j])
        
        AA = A
        BB = B
        CC = C
        DD = D

        A = round1(A,B,C,D,  X[0], 3)  
        D = round1(D,A,B,C,  X[1], 7) 
        C = round1(C,D,A,B,  X[2], 11)  
        B = round1(B,C,D,A,  X[3], 19)
        A = round1(A,B,C,D,  X[4], 3)  
        D = round1(D,A,B,C,  X[5], 7)
        C = round1(C,D,A,B,  X[6], 11)  
        B = round1(B,C,D,A,  X[7], 19)
        A = round1(A,B,C,D,  X[8], 3)  
        D = round1(D,A,B,C,  X[9], 7) 
        C = round1(C,D,A,B, X[10], 11)  
        B = round1(B,C,D,A, X[11], 19)
        A = round1(A,B,C,D, X[12], 3)  
        D = round1(D,A,B,C, X[13], 7)
        C = round1(C,D,A,B, X[14], 11)  
        B = round1(B,C,D,A, X[15], 19)

        A = round2(A,B,C,D,  X[0], 3)  
        D = round2(D,A,B,C,  X[4], 5) 
        C = round2(C,D,A,B,  X[8], 9)  
        B = round2(B,C,D,A,  X[12], 13)
        A = round2(A,B,C,D,  X[1], 3)  
        D = round2(D,A,B,C,  X[5], 5)
        C = round2(C,D,A,B,  X[9], 9)  
        B = round2(B,C,D,A,  X[13], 13)
        A = round2(A,B,C,D,  X[2], 3)  
        D = round2(D,A,B,C,  X[6], 5) 
        C = round2(C,D,A,B, X[10], 9)  
        B = round2(B,C,D,A, X[14], 13)
        A = round2(A,B,C,D, X[3], 3)  
        D = round2(D,A,B,C, X[7], 5)
        C = round2(C,D,A,B, X[11], 9)  
        B = round2(B,C,D,A, X[15], 13)

        A = round3(A,B,C,D,  X[0], 3)  
        D = round3(D,A,B,C,  X[8], 9) 
        C = round3(C,D,A,B,  X[4], 11)  
        B = round3(B,C,D,A,  X[12], 15)
        A = round3(A,B,C,D,  X[2], 3)  
        D = round3(D,A,B,C,  X[10], 9)
        C = round3(C,D,A,B,  X[6], 11)  
        B = round3(B,C,D,A,  X[14], 15)
        A = round3(A,B,C,D,  X[1], 3)  
        D = round3(D,A,B,C,  X[9],  9) 
        C = round3(C,D,A,B, X[5], 11)  
        B = round3(B,C,D,A, X[13], 15)
        A = round3(A,B,C,D, X[3], 3)  
        D = round3(D,A,B,C, X[11], 9)
        C = round3(C,D,A,B, X[7], 11)  
        B = round3(B,C,D,A, X[15], 15)

        A = mod_wrap(A + AA)
        B = mod_wrap(B + BB)
        C = mod_wrap(C + CC)
        D = mod_wrap(D + DD)
    
    return binascii.hexlify(struct.pack('<4I', A, B, C, D)).decode()

def pwn_prefix_md4(md4, plain, suffix, len_key):
    md4 = binascii.unhexlify(md4)
    (A,B,C,D) = struct.unpack('<4I', md4)
    temp = md_pad(md_pad(b"a"*len_key + plain) + suffix)

    block = temp[-64:]

    words = [int.from_bytes(block[0+i:4+i], "little") for i in range(0, len(block), 4)]
    X = []
    for j in range(16) :
        X.append(words[j])
    
    AA = A
    BB = B
    CC = C
    DD = D

    A = round1(A,B,C,D,  X[0], 3)  
    D = round1(D,A,B,C,  X[1], 7) 
    C = round1(C,D,A,B,  X[2], 11)  
    B = round1(B,C,D,A,  X[3], 19)
    A = round1(A,B,C,D,  X[4], 3)  
    D = round1(D,A,B,C,  X[5], 7)
    C = round1(C,D,A,B,  X[6], 11)  
    B = round1(B,C,D,A,  X[7], 19)
    A = round1(A,B,C,D,  X[8], 3)  
    D = round1(D,A,B,C,  X[9], 7) 
    C = round1(C,D,A,B, X[10], 11)  
    B = round1(B,C,D,A, X[11], 19)
    A = round1(A,B,C,D, X[12], 3)  
    D = round1(D,A,B,C, X[13], 7)
    C = round1(C,D,A,B, X[14], 11)  
    B = round1(B,C,D,A, X[15], 19)


    A = round2(A,B,C,D,  X[0], 3)  
    D = round2(D,A,B,C,  X[4], 5) 
    C = round2(C,D,A,B,  X[8], 9)  
    B = round2(B,C,D,A,  X[12], 13)
    A = round2(A,B,C,D,  X[1], 3)  
    D = round2(D,A,B,C,  X[5], 5)
    C = round2(C,D,A,B,  X[9], 9)  
    B = round2(B,C,D,A,  X[13], 13)
    A = round2(A,B,C,D,  X[2], 3)  
    D = round2(D,A,B,C,  X[6], 5) 
    C = round2(C,D,A,B, X[10], 9)  
    B = round2(B,C,D,A, X[14], 13)
    A = round2(A,B,C,D, X[3], 3)  
    D = round2(D,A,B,C, X[7], 5)
    C = round2(C,D,A,B, X[11], 9)  
    B = round2(B,C,D,A, X[15], 13)

    A = round3(A,B,C,D,  X[0], 3)  
    D = round3(D,A,B,C,  X[8], 9) 
    C = round3(C,D,A,B,  X[4], 11)  
    B = round3(B,C,D,A,  X[12], 15)
    A = round3(A,B,C,D,  X[2], 3)  
    D = round3(D,A,B,C,  X[10], 9)
    C = round3(C,D,A,B,  X[6], 11)  
    B = round3(B,C,D,A,  X[14], 15)
    A = round3(A,B,C,D,  X[1], 3)  
    D = round3(D,A,B,C,  X[9],  9) 
    C = round3(C,D,A,B, X[5], 11)  
    B = round3(B,C,D,A, X[13], 15)
    A = round3(A,B,C,D, X[3], 3)  
    D = round3(D,A,B,C, X[11], 9)
    C = round3(C,D,A,B, X[7], 11)  
    B = round3(B,C,D,A, X[15], 15)

    A = mod_wrap(A + AA)
    B = mod_wrap(B + BB)
    C = mod_wrap(C + CC)
    D = mod_wrap(D + DD)


    return binascii.hexlify(struct.pack('<4I', A, B, C, D)).decode()


if __name__ == "__main__":
    #print(md4(b"a"))
    prefix = b"idksomethinghere"
    msg = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    sha = md4(prefix+msg)
    print(sha)
    suffix = b";admin=true"
    pwned = pwn_prefix_md4(sha, msg, suffix, len(prefix))
    print(pwned)
    after_pwned = md4(md_pad( prefix + msg ) + suffix)
    print(after_pwned)