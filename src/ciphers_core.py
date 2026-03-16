"""
Core encryption and decryption algorithms for the ciphers.
Includes Caesar, Affine, and Transposition ciphers.
"""

from utils import is_english_alpha, mod_inverse

def encrypt_caesar(plaintext, shift):
    """Encrypt plaintext using Caesar cipher with the given shift."""
    ciphertext = []
    for char in plaintext:
        if is_english_alpha(char):
            base = ord('A') if char.isupper() else ord('a')
            # Shift the character within the 0-25 range, then add base ASCII back
            shifted_char = chr((ord(char) - base + shift) % 26 + base)
            ciphertext.append(shifted_char)
        else:
            ciphertext.append(char)
    return ''.join(ciphertext)

def decrypt_caesar(ciphertext, shift):
    """Decrypt ciphertext using Caesar cipher with the given shift."""
    # Decryption is just encryption with a negative shift
    return encrypt_caesar(ciphertext, -shift)

def encrypt_affine(plaintext, a, b):
    """
    Encrypt plaintext using Affine cipher.
    Formula: E(x) = (ax + b) mod 26
    """
    ciphertext = []
    for char in plaintext:
        if is_english_alpha(char):
            base = ord('A') if char.isupper() else ord('a')
            x = ord(char) - base
            encrypted_val = (a * x + b) % 26
            ciphertext.append(chr(encrypted_val + base))
        else:
            ciphertext.append(char)
    return ''.join(ciphertext)

def decrypt_affine(ciphertext, a, b):
    """
    Decrypt ciphertext using Affine cipher.
    Formula: D(x) = a^-1 * (x - b) mod 26
    """
    a_inv = mod_inverse(a, 26)
    plaintext = []
    for char in ciphertext:
        if is_english_alpha(char):
            base = ord('A') if char.isupper() else ord('a')
            x = ord(char) - base
            decrypted_val = (a_inv * (x - b)) % 26
            plaintext.append(chr(decrypted_val + base))
        else:
            plaintext.append(char)
    return ''.join(plaintext)

def encrypt_transposition(plaintext, column):
    """
    Encrypt plaintext using Transposition cipher.
    Whitespace characters are preserved. Pads the text with spaces if 
    it does not perfectly fill the grid.
    """
    if column <= 0:
        raise ValueError("Column size must be strictly positive.")
    
    # Calculate required padding to completely fill the matrix
    padding_length = (column - (len(plaintext) % column)) % column
    padded_text = plaintext + (' ' * padding_length)
    
    ciphertext = []
    # Read column by column
    for col in range(column):
        for row_start in range(col, len(padded_text), column):
            ciphertext.append(padded_text[row_start])
            
    return ''.join(ciphertext)

def decrypt_transposition(ciphertext, column):
    """
    Decrypt ciphertext using Transposition cipher.
    Requires the ciphertext to be padded, meaning len(ciphertext) 
    must be fully divisible by column.
    """
    if column <= 0:
        raise ValueError("Column size must be strictly positive.")
    
    num_rows = len(ciphertext) // column
    # The ciphertext is structured in blocks of size 'num_rows'.
    # We slice it into columns to easily reconstruct the rows.
    grid = [ciphertext[i:i + num_rows] for i in range(0, len(ciphertext), num_rows)]
    
    plaintext = []
    # Reconstruct the plaintext row by row
    for row in range(num_rows):
        for col in range(column):
            plaintext.append(grid[col][row])
            
    return ''.join(plaintext)