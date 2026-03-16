import subprocess
import os
import sys
import difflib

# Testlerin çalıştırılacağı dizinler
SRC_DIR = "."
IO_DIR = "/Users/aykutalpgurler/Downloads/BBM465_S26_PA1_IO_v1.0.1"
DICT_FILE = "/Users/aykutalpgurler/Downloads/BBM465_S26_PA1_dictionary_v1.txt"
OUTPUT_FOLDER = "test_results_out"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

TEST_CASES = [
    ("caesar_1_enc", ["python3", "cipher.py", "caesar", "e", f"{IO_DIR}/input_caesar_1.txt", "OUTPUT_PLACEHOLDER", "-s", "11"], f"{IO_DIR}/output_caesar_1_shift_11.txt"),
    ("caesar_2_enc", ["python3", "cipher.py", "caesar", "e", f"{IO_DIR}/input_caesar_2.txt", "OUTPUT_PLACEHOLDER", "-s", "7"], f"{IO_DIR}/output_caesar_2_shift_7.txt"),
    ("affine_1_enc", ["python3", "cipher.py", "affine", "e", f"{IO_DIR}/input_affine_1.txt", "OUTPUT_PLACEHOLDER", "-a", "5", "-b", "8"], f"{IO_DIR}/output_affine_1_a_5_b_8.txt"),
    ("affine_2_enc", ["python3", "cipher.py", "affine", "e", f"{IO_DIR}/input_affine_2.txt", "OUTPUT_PLACEHOLDER", "-a", "3", "-b", "5"], f"{IO_DIR}/output_affine_2_a_3_b_5.txt"),
    ("trans_1_enc", ["python3", "cipher.py", "transposition", "e", f"{IO_DIR}/input_transposition_1.txt", "OUTPUT_PLACEHOLDER", "-c", "5"], f"{IO_DIR}/output_transposition_1_column_5.txt"),
    ("trans_2_enc", ["python3", "cipher.py", "transposition", "e", f"{IO_DIR}/input_transposition_2.txt", "OUTPUT_PLACEHOLDER", "-c", "7"], f"{IO_DIR}/output_transposition_2_column_7.txt"),
    
    ("caesar_1_break", ["python3", "break.py", DICT_FILE, "caesar", f"{IO_DIR}/cryptanalysis_cipher_1_caesar_shift_13.txt", "OUTPUT_PLACEHOLDER"], f"{IO_DIR}/cryptanalysis_plain_1.txt"),
    ("caesar_2_break", ["python3", "break.py", DICT_FILE, "caesar", f"{IO_DIR}/cryptanalysis_cipher_2_caesar_shift_3.txt", "OUTPUT_PLACEHOLDER"], f"{IO_DIR}/cryptanalysis_plain_2.txt"),
    ("affine_1_break", ["python3", "break.py", DICT_FILE, "affine", f"{IO_DIR}/cryptanalysis_cipher_1_affine_a_9_b_2.txt", "OUTPUT_PLACEHOLDER"], f"{IO_DIR}/cryptanalysis_plain_1.txt"),
    ("affine_2_break", ["python3", "break.py", DICT_FILE, "affine", f"{IO_DIR}/cryptanalysis_cipher_2_affine_a_11_b_7.txt", "OUTPUT_PLACEHOLDER"], f"{IO_DIR}/cryptanalysis_plain_2.txt"),
    ("trans_1_break", ["python3", "break.py", DICT_FILE, "transposition", f"{IO_DIR}/cryptanalysis_cipher_1_transposition_column_100.txt", "OUTPUT_PLACEHOLDER"], f"{IO_DIR}/cryptanalysis_plain_1.txt"),
    ("trans_2_break", ["python3", "break.py", DICT_FILE, "transposition", f"{IO_DIR}/cryptanalysis_cipher_2_transposition_column_270.txt", "OUTPUT_PLACEHOLDER"], f"{IO_DIR}/cryptanalysis_plain_2.txt")
]

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.readlines() # Diff için satır satır okuyoruz

def main():
    print(f"Starting automated test suite. Results will be saved in '{OUTPUT_FOLDER}/'\n" + "="*50)
    passed, failed = 0, 0

    for test_id, cmd, expected_file in TEST_CASES:
        current_out = os.path.join(OUTPUT_FOLDER, f"my_out_{test_id}.txt")
        actual_cmd = [c.replace("OUTPUT_PLACEHOLDER", current_out) for c in cmd]
        
        print(f"Running {test_id}...", end=" ", flush=True)
        try:
            result = subprocess.run(actual_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"\n  [FAIL] Runtime Error:\n{result.stderr}")
                failed += 1
                continue
                
            gen_lines = read_file(current_out)
            exp_lines = read_file(expected_file)
            
            if gen_lines == exp_lines:
                print("PASSED")
                passed += 1
            else:
                print("FAILED (Content Mismatch)")
                # Diff üret ve terminale bas
                diff = difflib.unified_diff(
                    exp_lines, gen_lines, 
                    fromfile='Expected', tofile='Generated', 
                    lineterm=''
                )
                print("\n--- Differences Found ---")
                for line in diff:
                    print(line)
                print("--------------------------\n")
                failed += 1
                
        except Exception as e:
            print(f"\n  [ERROR] Exception: {e}")
            failed += 1

    print("="*50)
    print(f"FINAL RESULTS: {passed} Passed | {failed} Failed")

if __name__ == "__main__":
    main()