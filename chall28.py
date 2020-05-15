import struct

def mod_wrap(num, bitlen=32):
    return num & ((1<<bitlen) - 1)

def leftrotate(num, shift, bitlen = 32):
    return ((num << shift) & ((1<<bitlen) - 1)) | (num >> (bitlen - shift))

def sha1_pad(plain):
    bitlength = len(plain) * 8
    plain += b"\x80"
    end = (bitlength + 1) % 512
    if end > 448:
        add = (512-end+448)
        plain += b"\x00"*(add//8)
    else:
        add = (448-end) 
        plain += b"\x00"*(add//8)
    plain += struct.pack(">Q", bitlength)
    return plain

def sha1(plain):
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    plain = sha1_pad(plain)

    blocks = [plain[0+i:64+i] for i in range(0, len(plain), 64)]
    for block in blocks:
        w = [ int.from_bytes(block[0+i:4+i], "big") for i in range(0, len(block), 4)]
        for i in range( 16, 80):
            w += [leftrotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1)]
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        for i in range(80):
            if 0 <= i <= 19 :
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39 :
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d) 
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            temp = mod_wrap( leftrotate(a,5) + f + e + k + w[i] )
            e = d
            d = c
            c = leftrotate(b,30)
            b = a
            a = temp

        h0 = mod_wrap( h0 + a )
        h1 = mod_wrap( h1 + b ) 
        h2 = mod_wrap( h2 + c )
        h3 = mod_wrap( h3 + d )
        h4 = mod_wrap( h4 + e )

    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

if __name__ == "__main__":
    print(sha1(b"loli"))