alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def caesar_enc(letter, k=3):
    if letter < 'A' or letter > 'Z':
        print('Invalid letter')
        return None
    else:
        return alphabet[(ord(letter) - ord('A') + k) % len(alphabet)]


def caesar_enc_string(plaintext, k=3):
    ciphertext = ''
    for letter in plaintext:
        ciphertext = ciphertext + caesar_enc(letter, k)
    return ciphertext


def caesar_dec(letter, k=3):
    if letter < 'A' or letter > 'Z':
        print("Invalid letter")
        return
    else:
        return alphabet[(ord(letter) - ord('A') - k) % len(alphabet)]


def caesar_dec_string(plaintext, k=3):
    ciphertext = ''
    for letter in plaintext:
        ciphertext = ciphertext + caesar_dec(letter, k)
    return ciphertext


def main():
    message = input("Enter a message: ")
    shift_value = int(input("Choose the shift value: a number between 1 and 25: "))
    choice = input("Choose what you want: encrypt or decrypt?: ")
    message = message.upper()  # to be sure we'll have uppercase letters

    while 1:
        if choice == 'encrypt':
            ciphertext = caesar_enc_string(message, shift_value)
            print("The ciphertext is: " + ciphertext)
            break
        elif choice == 'decrypt':
            plaintext = caesar_dec_string(message, shift_value)
            print("The plaintext is: " + plaintext)
            break
        else:
            print("Please, choose between 'encrypt' or 'decrypt'!");
            choice = input("Choose what you want: encrypt or decrypt?: ")


if __name__ == "__main__":
    main()
    # input: decrypt(HWNUYTQTLNJ) -> CRIPTOLOGIE
