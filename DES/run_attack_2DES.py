"""
   *** This is an implementation of MEET-IN-THE-MIDDLE ATTACK against 2DES ***

  We know:
    --- 2 pairs of <plaintext, ciphertext>;
    --- last six bytes from key1 and key2;
    --- the length of a key is 8 bytes;

  We need to search for the first 2 bytes of the each key!

"""

from operator import itemgetter
import bisect
from DES2 import *

def get_index(a, x):
    """Locate the leftmost value exactly equal to x in list a"""
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
        return -1

def meet_in_the_middle(m1, m2, c1, c2, k1, k2):

    tb = []

    # Find all pairs (key, ciphertext) for message m1 and k2

    for byte1 in range(256):
        for byte2 in range(256):
            key = chr(byte1) + chr(byte2) + k2[2:]
            key_bytes = bytes(key, 'raw_unicode_escape')
            m1_bytes = bytes(m1, 'raw_unicode_escape')
            T = des_enc(key_bytes, m1_bytes)
            tb.append((key_bytes, T))

    # Sort list by T values(to use binary search)

    tbs = sorted(tb, key=itemgetter(1))

    # Select the second column for binary search

    tenc = [value for _,value in tbs]

    # Find the pair (k1, k2)

    for byte1 in range(256):
        for byte2 in range(256):
            key = chr(byte1) + chr(byte2) + k1[2:]
            key_bytes = bytes(key, 'raw_unicode_escape')
            c1_bytes = bytes(hex_2_str(c1), 'raw_unicode_escape')
            m2_bytes = bytes(m2, 'raw_unicode_escape')
            T = des_dec(key_bytes, c1_bytes)
            find_a_match = get_index(tenc,T)
            if find_a_match != -1:
                k2 = tbs[find_a_match][0]
                ciphertext = des2_enc(key_bytes, k2, m2_bytes).hex()
                if ciphertext == c2:
                    return key, bytes_to_string(k2)


def main():

    # TODO 3.D: run meet-in-the-middle attack for the following plaintext/ciphertext
    m1 = 'Pocainta'
    c1 = '9f98dbd6fe5f785d'
    m2 = 'Iertarea'
    c2 = '6e266642ef3069c2'

    # NOTE: you only need to search for the first 2 bytes of the each key (i.e.,
    # to find out what are the values for each `?`)
    k1 = '??oIkvH5'
    k2 = '??GK4EoU'
 
    # Run the attack against 2DES encryption:
    key1, key2 = meet_in_the_middle(m1, m2, c1, c2, k1, k2)

    msg = bytes_to_string(des2_dec(string_to_bytes(key1), string_to_bytes(key2),
                            bytes.fromhex(c1)))
    if(m1 == msg):
        print("The attack succeeded!")
        print("The keys are: k1 = {} and k2 = {}".format(key1, key2))
    else:
        print("Try again :((")

if __name__== '__main__':
    main()
