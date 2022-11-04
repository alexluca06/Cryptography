import base64
import utils

C1 = "010101100110000101101100011010000110000101101100011011000110000100100001"
C2 = "526f636b2c2050617065722c2053636973736f727321"
C3 = "WW91IGRvbid0IG5lZWQgYSBrZXkgdG8gZW5jb2RlIGRhdGEu"

# TODO: Decode the strings
P1 = utils.bin_2_str(utils.string_to_bytes(C1))
P2 = utils.hex_2_str(utils.string_to_bytes(C2))
P3 = utils.b64decode(C3)

print('P1 = ', P1)
print('P2 = ', P2)
print('P3 = ', P3)
