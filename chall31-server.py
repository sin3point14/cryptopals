from flask import Flask, request, abort
from chall28 import sha1
from binascii import unhexlify
from time import sleep
import os
app = Flask(__name__)

# key = os.urandom(64)
key = b'lol'
articial_sleep = 0.05

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

    return hash(o_key_pad + unhexlify(hash(i_key_pad + message)))

def insecure_compare(a,b):
    global articial_sleep
    for i,j in zip(a,b):
        sleep(articial_sleep)
        if i != j:
            return False
    return True

@app.route('/test')
def pwn():
    file = request.args.get('file') 
    signature = request.args.get('signature') 
    
    print(file.encode('utf-8'))
    global key
    file_hmac = hmac(key, file.encode('utf-8'), sha1, 64)

    if insecure_compare(file_hmac, signature):
        abort(200)
    else:
        abort(500)

if __name__ == '__main__':
    app.run(port=8082)