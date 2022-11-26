from Crypto.Cipher import DES
from utils import *

def des_enc(k, m):
    """
    Encrypt a message m with a key k using DES as follows:
    c = DES(k, m)

    Args:
        m should be a bytestring (i.e. a sequence of characters such as 'Hello'
          or '\x02\x04')
        k should be a bytestring of length exactly 8 bytes.

    Note that for DES the key is given as 8 bytes, where the last bit of
    each byte is just a parity bit, giving the actual key of 56 bits, as
    expected for DES. The parity bits are ignored.

    Return:
        The bytestring ciphertext c
    """
    d = DES.new(k, DES.MODE_ECB)
    c = d.encrypt(m)
    return c


def des_dec(k, c):
    """
    Decrypt a message c with a key k using DES as follows:
    m = DES(k, c)

    Args:
        c should be a bytestring (i.e. a sequence of characters such as 'Hello'
          or '\x02\x04')
        k should be a bytestring of length exactly 8 bytes.

    Note that for DES the key is given as 8 bytes, where the last bit of
    each byte is just a parity bit, giving the actual key of 56 bits, as
    expected for DES. The parity bits are ignored.

    Return:
        The bytestring plaintext m
    """
    d = DES.new(k, DES.MODE_ECB)
    m = d.decrypt(c)
    return m

"""
    Implement 2DES using DES implementation from above :
        2DES((k1,k2), m) = DES(k1, DES(k2, m))

"""

def des2_enc(k1, k2, m):
    # TODO 3.B: implement des2_enc
    return des_enc(k1, des_enc(k2, m))


def des2_dec(k1, k2, c):
    # TODO 3.B: implement des2_dec
    return des_dec(k2, des_dec(k1, c))

def main():
    k1 = 'Smerenie'
    k2 = 'Dragoste'
    m1_given = 'Fericiti cei saraci cu duhul, ca'
    c1 = 'cda98e4b247612e5b088a803b4277710f106beccf3d020ffcc577ddd889e2f32'
    c2 = '54826ea0937a2c34d47f4595f3844445520c0995331e5d492f55abcf9d8dfadf'

    # TODO 3.C: Decrypt c1 and c2 using k1 and k2, and make sure that 
    #           des2_dec(k1, k2, c1 || c2) == m1 || m2
    #
    # Note: The code to decrypt c1 is already provided below. You **need**
    # to decrypt c2 as well.
    

    m1 = bytes_to_string(des2_dec(string_to_bytes(k1), string_to_bytes(k2),
                            bytes.fromhex(c1)))
    assert m1 == m1_given, f'Expected "{m1_given}", but got "{m1}"'

    m2 = bytes_to_string(des2_dec(string_to_bytes(k1), string_to_bytes(k2),
                            bytes.fromhex(c2)))

    print("Plaintext: " + m1 +" "+ m2)

if __name__== '__main__':
    main()
