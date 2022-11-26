from math import ceil
import base64
import os
from random import randint
from Crypto.Cipher import AES
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
backend = default_backend()


def split_bytes_in_blocks(x, block_size):
    nb_blocks = ceil(len(x)/block_size)
    return [x[block_size*i:block_size*(i+1)] for i in range(nb_blocks)]
 
 
def pkcs7_padding(message, block_size):
    padding_length = block_size - (len(message) % block_size)
    if padding_length == 0:
        padding_length = block_size
    padding = bytes([padding_length]) * padding_length
    return message + padding
 
 
def pkcs7_strip(data):
    padding_length = data[-1]
    return data[:- padding_length]
 
 
def encrypt_aes_128_ecb(msg, key):
    padded_msg = pkcs7_padding(msg, block_size=16)
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    return encryptor.update(padded_msg) + encryptor.finalize()
 
 
def decrypt_aes_128_ecb(ctxt, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ctxt) + decryptor.finalize()
    message = pkcs7_strip(decrypted_data)
    return message
 
# You are not suppose to see this
class Oracle:
    def __init__(self):
        self.key = 'Mambo NumberFive'.encode()
        self.prefix = 'PREF'.encode()
        self.target = base64.b64decode(  # You are suppose to break this
            "RG8gbm90IGxheSB1cCBmb3IgeW91cnNlbHZlcyB0cmVhc3VyZXMgb24gZWFydGgsIHdoZXJlIG1vdGggYW5kIHJ1c3QgZGVzdHJveSBhbmQgd2hlcmUgdGhpZXZlcyBicmVhayBpbiBhbmQgc3RlYWwsCmJ1dCBsYXkgdXAgZm9yIHlvdXJzZWx2ZXMgdHJlYXN1cmVzIGluIGhlYXZlbiwgd2hlcmUgbmVpdGhlciBtb3RoIG5vciBydXN0IGRlc3Ryb3lzIGFuZCB3aGVyZSB0aGlldmVzIGRvIG5vdCBicmVhayBpbiBhbmQgc3RlYWwuCkZvciB3aGVyZSB5b3VyIHRyZWFzdXJlIGlzLCB0aGVyZSB5b3VyIGhlYXJ0IHdpbGwgYmUgYWxzby4="
        )
 
    def encrypt(self, message):
        return encrypt_aes_128_ecb(
            self.prefix + message + self.target,
            self.key
        )
