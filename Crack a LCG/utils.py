def _chunks(string, chunk_size):
    for i in range(0, len(string), chunk_size):
        yield string[i:i+chunk_size]
 
def _hex(x):
    return format(x, '02x')

def hexxor(a, b):  # xor two hex-strings, trims the longer input
    return ''.join(_hex(int(x, 16) ^ int(y, 16)) for (x, y) in zip(_chunks(a, 2), _chunks(b, 2)))
 
def str_2_hex(data):
    return ''.join(f'{ord(c):02x}' for c in data)

def hex_2_str(data):
    return ''.join(chr(int(x, 16)) for x in _chunks(data, 2))