from chall11 import encrypt_aes_cbc,pkcs7_padding

iv = bytes.fromhex('216383836370f515da127e30d0df9ed9')
pt = b'aaaaaaaaaaaaaaa'
key = iv

print(encrypt_aes_cbc(pkcs7_padding(pt, 16), key, iv).hex())