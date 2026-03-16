"""
Utility functions for Information Security Laboratory Project 1.
Provides file I/O, mathematical operations, and character checks.
"""

def read_file(filepath):
    """Read and return the contents of a file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(filepath, content):
    """Write the given content to a file."""
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

def is_english_alpha(char):
    """
    Check if a character belongs to the English alphabet.
    Returns True for A-Z and a-z, False otherwise.
    """
    return ('a' <= char <= 'z') or ('A' <= char <= 'Z')

def mod_inverse(a, m):
    """
    Calculate the modular multiplicative inverse of 'a' modulo 'm'.
    Requires Python 3.8+ built-in pow() functionality.
    """
    try:
        return pow(a, -1, m)
    except ValueError:
        # Raised if a and m are not coprime
        raise ValueError(f"{a} and {m} are not coprime.")

def get_coprimes_of_26():
    """
    Return a list of integers between 1 and 25 that are coprime with 26.
    Used to optimize the affine cipher cryptanalysis search space.
    """
    return [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]

def load_dictionary(filepath):
    """
    Load a dictionary file into a set for O(1) lookup performance.
    Words are stripped of whitespace and converted to lowercase.
    """
    valid_words = set()
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip().lower()
            if word:
                valid_words.add(word)
    return valid_words