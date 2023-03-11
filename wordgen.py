import itertools
import argparse
import random

# --- Define sound constants ---

# Consonants
C = ['t', 'r', 's', 'sh', 'k', 'n', 'l', 'm', 'r', 'b', 'v', 'd']

# Final consonants
F = ['t', 's', 'k', 'n']

# Vowels
V = ['a', 'i', 'u', 'e']

# Clusters
CL = ['tr', 'kt', 'st', 'nt', 'nd']

# --- Generate all possible words ---

# Rules:
# - Word must not start with a consonant cluster
# - Word must end with a vowel or final consonant

def gen_words(syl: int) -> list[str]:
    # Generate all possible CV syllables
    CV = fork(C, V)

    # Generate all possible CLV syllables
    CLV = fork(CL, V)
    
    # Each word must start with a CV syllable or a vowel
    words = CV + V

    # Append new syllables until we reach the desired length
    for i in range(syl - 1):
        # Syllables in the middle of the word can either be CV or CLV
        words = fork(words, CV + CLV)
        
    # Append the final consonant but also leave a version wihout it
    words = words + fork(words, F)
        
    return words

# Create new versions of words by appending all possible endings to them
# Example: fork(['a', 'b'], ['c', 'd']) = ['ac', 'ad', 'bc', 'bd']

def fork(words: list[str], endings: list[str]) -> list[str]:
    return [''.join(pair) for pair in list(itertools.product(words, endings))]

# --- Conjugate ---

def conjugate(word: str) -> list[str]:
    return [word, word + 'en', word + 'at', word + 'ur']

# --- Command line interface ---

# I used an external library to parse the command line arguments
def main():
    parser = argparse.ArgumentParser(
        prog='wordgen',
        description='Generate possible words based on some internal rules.')

    parser.add_argument(
        'syllables',
        type=int,
        help='The number of syllables the words should contain.')

    parser.add_argument(
        '-n',
        '--number',
        action='store',
        type=int,
        help='The number of generated words to output. If not specified, output all words.')

    parser.add_argument(
        '-r',
        '--random',
        action='store_true',
        help='Randomize the order of the words.')

    parser.add_argument(
        '-c',
        '--conjugate',
        action='store_true',
        help='Generate conjugated forms for each word.')

    args = parser.parse_args()

    words = gen_words(args.syllables)

    if args.random:
        random.shuffle(words)

    if not args.number == None:
        words = words[:args.number]

    if args.conjugate:
        words = [' '.join(conjugate(word)) for word in words]

    print('\n'.join(words))

if __name__ == '__main__':
    main()
