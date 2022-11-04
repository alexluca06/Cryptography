alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
shift_value = 3


# Function that encrypt a single letter with a shift value

def caesar_enc(letter):
    if (letter < 'A' or letter > 'Z') and letter != " ":
        print('Invalid letter')
        return
    elif letter == " ":
        return " "
    else:
        return alphabet[(ord(letter) - ord('A') + shift_value) % len(alphabet)]


# Function that encrypt a string using caesar_enc for a letter

def caesar_enc_string(plaintext):
    ciphertext = ''
    for letter in plaintext:
        ciphertext = ciphertext + caesar_enc(letter)
    return ciphertext


# Function that decrypt a single letter with a shift value

def caesar_dec(letter):
    if (letter < 'A' or letter > 'Z') and letter != " ":
        print("Invalid letter")
        return
    elif letter == " ":
        return " "
    else:
        return alphabet[(ord(letter) - ord('A') - shift_value) % len(alphabet)]


# Function that decrypt a string using caesar_dec for a letter

def caesar_dec_string(plaintext):
    ciphertext = ''
    for letter in plaintext:
        ciphertext = ciphertext + caesar_dec(letter)
    return ciphertext


def main():

    message = input("Enter a message: ")
    choice = input("Choose what you want: encrypt or decrypt?: ")
    message = message.upper()  # to be sure we'll have uppercase letters

    while 1:
        if choice == 'encrypt':
            ciphertext = caesar_enc_string(message)
            print("The ciphertext is: " + ciphertext)
            break
        elif choice == 'decrypt':
            plaintext = caesar_dec_string(message)
            print("The plaintext is: " + plaintext)
            break
        else:
            print("Please, choose between 'encrypt' or 'decrypt'!");
            choice = input("Choose what you want: encrypt or decrypt?: ")


if __name__ == "__main__":
    main()
