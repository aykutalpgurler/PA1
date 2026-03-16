"""
Driver script for Cipher Implementation (Part 1).
Handles command-line arguments and executes encryption/decryption operations.
"""

import argparse
import sys
from utils import read_file, write_file
import ciphers_core

def main():
    parser = argparse.ArgumentParser(description="Basic Ciphers Encryption and Decryption Tool")
    
    # Positional arguments
    parser.add_argument("cipher", choices=["caesar", "affine", "transposition"], help="Cipher technique to be used")
    parser.add_argument("mode", choices=["e", "d"], help="Operation mode: 'e' for encrypt, 'd' for decrypt")
    parser.add_argument("input", help="Path to the input file")
    parser.add_argument("output", help="Path to the output file")
    
    # Optional arguments
    parser.add_argument("-s", type=int, help="Shift amount for Caesar cipher")
    parser.add_argument("-a", type=int, help="Parameter 'a' for Affine cipher")
    parser.add_argument("-b", type=int, help="Parameter 'b' for Affine cipher")
    parser.add_argument("-c", type=int, help="Number of columns for Transposition cipher")
    
    args = parser.parse_args()
    
    try:
        input_text = read_file(args.input)
    except FileNotFoundError:
        sys.exit(f"Error: Input file '{args.input}' not found.")

    result_text = ""

    # Caesar Cipher Handling
    if args.cipher == "caesar":
        if args.s is None:
            sys.exit("Error: Caesar cipher requires the '-s' (shift) argument.")
        if args.mode == "e":
            result_text = ciphers_core.encrypt_caesar(input_text, args.s)
        else:
            result_text = ciphers_core.decrypt_caesar(input_text, args.s)

    # Affine Cipher Handling
    elif args.cipher == "affine":
        if args.a is None or args.b is None:
            sys.exit("Error: Affine cipher requires both '-a' and '-b' arguments.")
        if args.mode == "e":
            result_text = ciphers_core.encrypt_affine(input_text, args.a, args.b)
        else:
            try:
                result_text = ciphers_core.decrypt_affine(input_text, args.a, args.b)
            except ValueError as e:
                sys.exit(f"Error during Affine decryption: {e}")

    # Transposition Cipher Handling
    elif args.cipher == "transposition":
        if args.c is None:
            sys.exit("Error: Transposition cipher requires the '-c' (column) argument.")
        if args.mode == "e":
            result_text = ciphers_core.encrypt_transposition(input_text, args.c)
        else:
            result_text = ciphers_core.decrypt_transposition(input_text, args.c)

    # Write the output
    write_file(args.output, result_text)

if __name__ == "__main__":
    main()