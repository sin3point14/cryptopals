from chall12 import *
def decrypt_aes_ecb(plain, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(plain)
def parse(a):
    parsed = dict()
    pairs = a.split('&')
    for i in pairs:
        first, second = i.split('=')
        parsed[first] = second
    return parsed
def profile_for(a):
    if b'&' not in a and b'=' not in a:
        return encrypt_aes_ecb(pkcs7_padding(b'email='+bytes(a)+b'&uid=10&role=user', 16),key)
    else:
        return False
def rev_profile(a):
    return parse(str(decrypt_aes_ecb(a, key)))
def i_iz_admin():
    pad = b"A"*10
    payload = pad + b"admin" + bytes([11])*11
    admin_encrypted = profile_for(payload)[16:32]
    payload = b"foo@bar.co.in"
    raw = profile_for(payload)[:-16]
    print(rev_profile(raw+admin_encrypted))

if __name__ == "__main__":
    print(parse('foo=bar&baz=qux&zap=zazzle'))
    print(profile_for(b"foo@bar.com"))
    i_iz_admin()