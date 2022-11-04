import utils

C1 = "000100010001000000001100000000110001011100000111000010100000100100011101000001010001100100000101"
C2 = "02030F07100A061C060B1909"

key = "abcdefghijkl"

# Utils functions

def _chunks(string, chunk_size):
    for i in range(0, len(string), chunk_size):
        yield string[i:i+chunk_size]
        
def strxor(a, b):  # xor two strings, trims the longer input
    return ''.join(chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b))
    
def bin_2_str(data):
    return ''.join(chr(int(b, 2)) for b in _chunks(data, 8))
 
def hex_2_str(data):
    return ''.join(chr(int(x, 16)) for x in _chunks(data, 2))
    

# TODO: Compute P1 and P2, from C1 and C2 respectively, using the key "abcdefghijkl"
P1 = strxor(bin_2_str(C1), key)
P2 = strxor(hex_2_str(C2), key)

print('P1 = ', P1)
print('P2 = ', P2)
