from chall18 import aes_ctr
import os, base64

CHARACTER_FREQ = {
    'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,
    'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,
    'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
    'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
}
def singlechar_xor(input_bytes, key_value):
    output = b''
    for char in input_bytes:
        output += bytes([char ^ key_value])
    return output

def get_english_score(input_bytes):
    score = 0
    for byte in input_bytes:
        score += CHARACTER_FREQ.get(chr(byte).lower(), 0)
    return score

def singlechar_xor_brute_force(ciphertext):
    candidates = []
    for key_candidate in range(256):
        plaintext_candidate = singlechar_xor(ciphertext, key_candidate)
        candidate_score = get_english_score(plaintext_candidate)
        result = {
            'key': key_candidate,
            'score': candidate_score,
            'plaintext': plaintext_candidate
        }
        candidates.append(result)
    return sorted(candidates, key=lambda c: c['score'], reverse=True)[0]

plains = [b'SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==', b'Q29taW5nIHdpdGggdml2aWQgZmFjZXM=', b'RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==', b'RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=', b'SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk', b'T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==', b'T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=', b'UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==', b'QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=', b'T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl', b'VG8gcGxlYXNlIGEgY29tcGFuaW9u', b'QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==', b'QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=', b'QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==', b'QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=', b'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=', b'VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==', b'SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==', b'SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==', b'VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==', b'V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==', b'V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==', b'U2hlIHJvZGUgdG8gaGFycmllcnM/', b'VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=', b'QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=', b'VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=', b'V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=', b'SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==', b'U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==', b'U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=', b'VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==', b'QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu', b'SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=', b'VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs', b'WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=', b'SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0', b'SW4gdGhlIGNhc3VhbCBjb21lZHk7', b'SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=', b'VHJhbnNmb3JtZWQgdXR0ZXJseTo=', b'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=']
key = bytes(bytearray(os.urandom(16)))
ciphers = []
for i in plains:
    print(i)
    i = base64.b64decode(i)
    ciphers.append(aes_ctr(i, key, 0))
lenghts = [len(x) for x in ciphers]
max_len = max(lenghts)
guessed_key =b''
for i in range(max_len):
    single_key_xor = b''.join([bytes([cipher[i]]) if len(cipher) > i else b'' for cipher in ciphers])
    guessed_key += bytes([singlechar_xor_brute_force(single_key_xor)["key"]])
for cipher in ciphers:
    print(bytes([b1 ^ b2 for b1, b2 in zip(cipher, guessed_key)]))