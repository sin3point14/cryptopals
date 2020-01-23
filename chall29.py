from chall28 import sha1, sha1_pad, leftrotate, mod_wrap

def pwn_prefix_sha1(sha, plain, suffix, len_key):
    h0 = int(sha[0:8], 16)
    h1 = int(sha[8:16], 16)
    h2 = int(sha[16:24], 16)
    h3 = int(sha[24:32], 16)
    h4 = int(sha[32:40], 16)

    temp = sha1_pad(sha1_pad(b"a"*len_key + plain) + suffix)
    block = temp[-64:]

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


prefix = b"idksomethinghere"
msg = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
sha = sha1(prefix+msg)
print(sha)
suffix = b";admin=true"
pwned = pwn_prefix_sha1(sha, msg, suffix, len(prefix))
print(pwned)
after_pwned = sha1(sha1_pad( prefix + msg ) + suffix)
print(after_pwned)