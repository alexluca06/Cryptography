import operator
from collections import Counter

# This is the list of bigrams, from most frequent to less frequent
bigrams = ["TH", "HE", 'IN', 'OR', 'HA', 'ET', 'AN',
           'EA', 'IS', 'OU', 'HI', 'ER', 'ST', 'RE', 'ND']

# This is the list of monograms, from most frequent to less frequent
monograms = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'R', 'H', 'D', 'L', 'U',
             'C', 'M', 'F', 'Y', 'W', 'G', 'P', 'B', 'V', 'K', 'X', 'Q', 'J', 'Z']

# This is the dictionary containing the substitution table (e.g. subst_table['A'] = 'B')
# TODO Fill it in the create_subst_table function
subst_table = {}

# These are the dictionaries containing the frequencies of the mono/bigrams in the text
# TODO Fill them in the analyze function
freq_table_bi = {}
freq_table_mono = {}


def sort_dictionary(d):
    """ Sorts a dictionary d by the value. Returns a list of tuples sorted
        by the second element. """
    sorted_dict = list(reversed(sorted(d.items(), key=operator.itemgetter(1))))
    return sorted_dict


def adjust():
    """ This is magic stuff used in main. """
    global subst_table
    subst_table['Y'] = 'B'
    subst_table['E'] = 'L'
    subst_table['L'] = 'M'
    subst_table['P'] = 'W'
    subst_table['F'] = 'C'
    subst_table['X'] = 'F'
    subst_table['J'] = 'G'
    subst_table['I'] = 'Y'


def analyze(text):
    """ Computes the frequencies of the monograms and bigrams in the text. """
    global freq_table_mono, freq_table_bi

    # TODO 1.1 Fill in the freq_table_mono dictionary
    freq_table_mono = dict(zip(monograms, [0] * 26))
    for letter in text:
        if letter in monograms:
            freq_table_mono[letter] += 1

    # TODO 1.2 Fill in the freq_table_bi dictionary

    freq_table_bi = dict(Counter(text[idx: idx + 2] for idx in range(len(text) - 2)))


def create_subst_table():
    """ Creates a substitution table using the frequencies of the bigrams. """
    global subst_table

    # TODO 2.1 Sort the bigrams frequency table by the frequency
    
    sorted_freq_table_bi = sort_dictionary(freq_table_bi)
    
    # TODO 2.2 Fill in the substitution table by associating the sorted frequency
    # dictionary with the given bigrams

    for i in range(len(bigrams)):
        if sorted_freq_table_bi[i][0][0] not in subst_table.keys():
            subst_table[sorted_freq_table_bi[i][0][0]] = bigrams[i][0]

        if sorted_freq_table_bi[i][0][1] not in subst_table.keys():
            subst_table[sorted_freq_table_bi[i][0][1]] = bigrams[i][1]


def complete_subst_table():
    """ Fills in the letters missing from the substitution table using the
        frequencies of the monograms. """
    global subst_table

    # TODO 3.1 Sort the monograms frequency table by the frequency
    
    sorted_freq_table_mono = sort_dictionary(freq_table_mono)

    # TODO 3.2 Fill in the missing letters from the substitution table by
    # associating the sorted frequency dictionary with the given monograms
    
    index = 0

    for key in monograms:
        if sorted_freq_table_mono[index][0] not in subst_table.keys():
            subst_table[sorted_freq_table_mono[index][0]] = key
        index += 1


def decrypt_text(text):
    global subst_table, subst_table

    # TODO 4 Decrypt and print the text using the substitution table
    plaintext = []

    # Replace the monograms:
    for i in range(len(text) - 1):
        plaintext.append(subst_table[text[i]])

    plaintext = "".join(plaintext)

    return plaintext

def main():
    with open('msg.txt', 'r') as myfile:
        text = myfile.read()

    analyze(text)
    create_subst_table()
    complete_subst_table()
    adjust()
    plaintext = decrypt_text(text)
    print(plaintext)

if __name__ == "__main__":
    main()
