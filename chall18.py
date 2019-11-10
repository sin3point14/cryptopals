from chall11 import encrypt_aes_ecb
import base64, struct

def aes_ctr(text, key, nonce):
    chunks, chunk_size = len(cipher), 16
    blocks = [ cipher[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
    ct = b''
    for i, block in enumerate(blocks):
        concat = struct.pack("<QQ", nonce, i)
        ct +=  bytes([b1 ^ b2 for b1, b2 in zip(encrypt_aes_ecb(concat, key), block)])
    return ct

cipher = base64.b64decode('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')
print(aes_ctr(cipher, "YELLOW SUBMARINE", 0))