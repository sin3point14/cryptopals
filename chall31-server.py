from flask import Flask, request
from chall28 import sha1
from binascii import unhexlify
app = Flask(__name__)

def xor(s1, s2):
    return b"".join([bytes([i1^i2]) for i1,i2 in zip(s1,s2)])

@app.route('/')
def hello_world():
    return 'Hello, World!'

def hmac(key,message,hash,blockSize):
 
    if len(key) > blockSize:
        key = hash(key)

    if len(key) < blockSize:
        key += b'\x00'*(blockSize - len(key))

    o_key_pad = xor(key, b'\x5c' * blockSize)
    i_key_pad = xor(key, b'\x36' * blockSize)

    print(o_key_pad)
    print(i_key_pad)

    print(hash(i_key_pad + message))

    return hash(o_key_pad + unhexlify(hash(i_key_pad + message)))

@app.route('/pwn')
def pwn():
    file = request.args.get('file') 
    sign = request.args.get('signature') 

    return "lol"