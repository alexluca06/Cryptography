import caesarCipher

def decrypt(ciphertext):
    
    plaintext = {}

    # TODO decrypt the ciphertext trying every possible shift value
    for key in range(1,26):
      plaintext[key] = caesarCipher.caesar_dec_string(ciphertext, key)
      
    return plaintext  # every possibilities


def main():
    
    ciphertexts = []

    with open("ciphertexts.txt", 'r') as f:
        for line in f:
            ciphertexts.append(line[:-1])

    # for every ciphertext, try all the shift values
    for c in ciphertexts:
        print(decrypt(c))

if __name__ == "__main__":
    main()