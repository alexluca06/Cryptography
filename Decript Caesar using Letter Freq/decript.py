import caesarCipher

freqs = {'A': 0.07048643054277828,
         'C': 0.01577161913523459,
         'B': 0.012074517019319227,
         'E': 0.13185372585096597,
         'D': 0.043393514259429625,
         'G': 0.01952621895124195,
         'F': 0.023867295308187673,
         'I': 0.06153403863845446,
         'H': 0.08655128794848206,
         'K': 0.007566697332106716,
         'J': 0.0017594296228150873,
         'M': 0.029657313707451703,
         'L': 0.04609015639374425,
         'O': 0.07679967801287949,
         'N': 0.060217341306347746,
         'Q': 0.0006382244710211592,
         'P': 0.014357175712971482,
         'S': 0.05892939282428703,
         'R': 0.05765294388224471,
         'U': 0.02749540018399264,
         'T': 0.09984475620975161,
         'W': 0.01892824287028519,
         'V': 0.011148804047838086,
         'Y': 0.023045078196872126,
         'X': 0.0005289788408463661,
         'Z': 0.00028173873045078196
         }

keylen = 7

def compute_distribution(f):
    """ Computes the chi-distribution based on a dictionary of frequencies
        relative to the freqs frequencies dictionary. """
    x2 = 0
    for l in freqs:
        x2 = x2 + (f[l] - freqs[l]) ** 2 / freqs[l]
    return x2


def split_in_cosets(text, keylen):
    """ Splits a text in keylen cosets. """
    cosets = []
    for i in range(keylen):
        coset = []
        for j in range(i, len(text), keylen):
            coset.append(text[j])
        cosets.append(coset)
    return cosets


def merge_cosets(cosets, coset_size):
    """ Merges the cosets to obtain the original text. """
    text = ''
    for j in range(coset_size):
        for i in range(len(cosets)):
            text = text + cosets[i][j]
    return text
 
    
def get_freq_dict(coset, shift):
    """ Computes the frequency table for a coset shifted to left with a given shift. """
    d = {}
    # TODO 1 compute the frequency of the letters in the coset shifted to left
    # by the shift parameter
    
    for letter in coset:
      shifted_letter = caesarCipher.caesar_dec(letter, shift)
      if shifted_letter in d.keys():
        d[shifted_letter] += 1 / len(coset)
      else:
        d[shifted_letter] = 1 / len(coset)
    return d


def find_correct_shift(coset):
    """ Returns the shift computed for a coset. """
   
    shift = 0
    lowest_chi_distr = 9999
   
    # TODO 2 compute the shift which leads to the lowest chi-distribution
   
    for i in range(0, 26):
      d = get_freq_dict(coset, i);
      min_value = compute_distribution(d)
      if min_value < lowest_chi_distr:
        lowest_chi_distr = min_value
        shift = i
    return shift
    
def main():

    with open('msg_ex3.txt', 'r') as myfile:
        text = myfile.read().strip()

    # TODO 3 decrypt the text

    text_splitted = split_in_cosets(text, keylen) # split the cipher text
    cosets = []

    for i in range(keylen):
        s = find_correct_shift(text_splitted[i])
        cosets.append(caesarCipher.caesar_dec_string(text_splitted[i], s))

    plaintext = merge_cosets(cosets, len(cosets[0]))
    print(plaintext)


if __name__ == "__main__":
    main()
