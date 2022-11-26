from utils import *
from oracle_aes import Oracle, split_bytes_in_blocks

# Task 1
def findBlockSize():
    initialLength = len(Oracle().encrypt(b''))
    i = 0
    while 1:  # Feed identical bytes of your-string to the function 1 at a time until you get the block length
        # You will also need to determine here the size of fixed prefix + target + pad
        # And the minimum size of the plaintext to make a new block
        length = len(Oracle().encrypt(b'X'*i))
        i += 1
        if length != initialLength:
          block_size = length - initialLength
          sizeOfPrefixTargetPadding = initialLength
          minimumSizeToAlighPlaintext = i-1
          return block_size, sizeOfPrefixTargetPadding, minimumSizeToAlighPlaintext


# Task 2
def findPrefixSize(block_size):
    previous_blocks = None
    # Find the situation where prefix_size + padding_size - 1 = block_size
    # Use split_bytes_in_blocks to get blocks of size(block_size)
    
    # Am luat doar primul block in calcul fiindca la rulari cu diferite inputuri
    # am observat ca dupa i > 12 primul block ramane neschimbat -> prefix == 4 bytes

    c = Oracle().encrypt(b"")
    blocks = split_bytes_in_blocks(c, block_size)
    previous_blocks = blocks[0]

    i = 1
    while 1:  
        c = Oracle().encrypt(b'X'*i)
        blocks = split_bytes_in_blocks(c, block_size)
        if previous_blocks == blocks[0]:
          prefix_size = block_size - (i - 1)
          return prefix_size
        i += 1
        previous_blocks = blocks[0]


# Task 3
def recoverOneByteAtATime(block_size, prefix_size, target_size):
    
    known_target_bytes = b""
    block_number = 0  # the block where the target byte is
    
    for _ in range(target_size):
        # prefix_size + padding_length + known_len + 1 = 0 mod block_size
        known_len = len(known_target_bytes)
        padding_length = (- known_len - 1 - prefix_size) % block_size
        padding = b"X" * padding_length
        # target block plaintext contains only known characters except its last character
        # Don't forget to use split_bytes_in_blocks to get the correct block
        input = padding
      
        c = Oracle().encrypt(input)  
        blocks = split_bytes_in_blocks(c, block_size)
        find_target_byte_from = blocks[block_number] 
        
        # trying every possibility for the last character
        for c in range(256):
          last_char = b"" + string_to_bytes(chr(c))
          new_input = padding + known_target_bytes  + last_char
          c = Oracle().encrypt(new_input)  # got the encryption for our bruteforce
          blocks = split_bytes_in_blocks(c, block_size)

          # when we find a match -> we find a byte from our target
          if find_target_byte_from == blocks[block_number]:
            known_target_bytes = known_target_bytes + last_char
            break

        # Go to the next block to find another bytes 
        if len(known_target_bytes) == (block_size*block_number + (block_size - prefix_size)):
          block_number = block_number+1
    
    return known_target_bytes.decode()


def main():

    # Find block size, prefix size, and length of plaintext size to allign blocks
    block_size, sizeOfPrefixTargetPadding, minimumSizeToAlignPlaintext = findBlockSize()
    print("Block size:\t\t\t\t" + str(block_size))
    print("Size of prefix, target, and padding:\t" + str(sizeOfPrefixTargetPadding))
    print("Pad needed to align:\t\t\t" + str(minimumSizeToAlignPlaintext))

    # Find size of the prefix
    prefix_size = findPrefixSize(block_size)
    print("\nPrefix Size:\t" + str(prefix_size))

    # Size of the target
    target_size = sizeOfPrefixTargetPadding - \
        minimumSizeToAlignPlaintext - prefix_size


    print("\nTarget:")
    print(recoverOneByteAtATime(block_size, prefix_size, target_size))

if __name__ == "__main__":
    main()