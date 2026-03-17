"""
Cryptanalysis algorithms for breaking basic ciphers.
Includes dictionary validation to identify the correct plaintext.
"""

import ciphers_core
from utils import get_coprimes_of_26, is_english_alpha

def score_text(text, valid_words_set):
    """
    Calculate a score based on how many valid dictionary words exist in the text.
    Longer valid words contribute more to the total score.
    """
    words = text.split()
    score = 0
    for word in words:
        # Strip punctuation to correctly match dictionary words
        clean_word = "".join([char for char in word if is_english_alpha(char)]).lower()
        if clean_word in valid_words_set:
            # Wiser methodology: Kelimenin harf sayısı kadar puan ekle
            score += len(clean_word)
    return score

def break_caesar(ciphertext, valid_words_set):
    """
    Break Caesar cipher by testing all possible 26 shift values.
    Returns the plaintext with the highest dictionary validation score.
    """
    best_score = -1
    best_plaintext = ""
    
    for shift in range(26):
        candidate = ciphers_core.decrypt_caesar(ciphertext, shift)
        score = score_text(candidate, valid_words_set)
        
        if score > best_score:
            best_score = score
            best_plaintext = candidate
            
    return best_plaintext

def break_affine(ciphertext, valid_words_set):
    """
    Break Affine cipher by testing all valid key pairs.
    Optimization: Only tests 'a' values that are coprime with 26.
    Returns the plaintext with the highest dictionary validation score.
    """
    best_score = -1
    best_plaintext = ""
    valid_a_values = get_coprimes_of_26()
    
    for a in valid_a_values:
        for b in range(26):
            try:
                candidate = ciphers_core.decrypt_affine(ciphertext, a, b)
                score = score_text(candidate, valid_words_set)
                
                if score > best_score:
                    best_score = score
                    best_plaintext = candidate
            except ValueError:
                # Should not happen as we only use valid coprimes, but safe to catch
                continue
                
    return best_plaintext

def break_transposition(ciphertext, valid_words_set):
    """
    Break Transposition cipher by testing possible column sizes.
    Returns the plaintext with the highest dictionary validation score.
    """
    best_score = -1
    best_plaintext = ""
    max_columns = len(ciphertext)
    
    # Column size can range from 1 to the length of the ciphertext
    for column in range(1, max_columns + 1):
        # Transposition decryption requires ciphertext length to be divisible by column
        if len(ciphertext) % column != 0:
            continue
            
        candidate = ciphers_core.decrypt_transposition(ciphertext, column)
        score = score_text(candidate, valid_words_set)
        
        if score > best_score:
            best_score = score
            best_plaintext = candidate
            
    # Wiser methodology: Sona eklenen padding boşluklarını temizleyerek 
    # orijinal dosya ile byte-by-byte match sağlıyoruz.
    return best_plaintext.rstrip(" ")