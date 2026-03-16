"""
Driver script for Cryptanalysis (Part 2).
Handles command-line arguments and executes cipher breaking operations.
"""

import argparse
import sys
from utils import read_file, write_file, load_dictionary
import cryptanalysis

def main():
    parser = argparse.ArgumentParser(description="Cryptanalysis Tool for Basic Ciphers")
    
    # Positional arguments strictly following the documentation
    parser.add_argument("dictionary", help="Path to the dictionary file")
    parser.add_argument("cipher", choices=["caesar", "affine", "transposition"], help="Cipher technique to be broken")
    parser.add_argument("input", help="Path to the input file containing ciphertext")
    parser.add_argument("output", help="Path to the output file for plaintext")
    
    args = parser.parse_args()
    
    # Load dictionary into a set for O(1) lookup
    try:
        valid_words_set = load_dictionary(args.dictionary)
    except FileNotFoundError:
        sys.exit(f"Error: Dictionary file '{args.dictionary}' not found.")
        
    # Read input ciphertext
    try:
        ciphertext = read_file(args.input)
    except FileNotFoundError:
        sys.exit(f"Error: Input file '{args.input}' not found.")
        
    plaintext = ""
    
    # Execute the appropriate breaking function
    if args.cipher == "caesar":
        plaintext = cryptanalysis.break_caesar(ciphertext, valid_words_set)
    elif args.cipher == "affine":
        plaintext = cryptanalysis.break_affine(ciphertext, valid_words_set)
    elif args.cipher == "transposition":
        plaintext = cryptanalysis.break_transposition(ciphertext, valid_words_set)
        
    # Warn if breaking was totally unsuccessful (e.g., empty result)
    if not plaintext:
        print("Warning: Could not find a highly probable plaintext with the given dictionary.")
    
    # Write the resulting plaintext to the output file
    write_file(args.output, plaintext)

if __name__ == "__main__":
    main()