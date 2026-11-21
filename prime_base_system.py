
#NO PERFECT SUM

import math

# --- 1. Setup and Sequence Generation ---

# Range of decimal values: 48 ('0') up to 90 ('Z')
N_MIN = 48
N_MAX = 90

# Mapping ASCII decimal values to their character representations
DECIMAL_TO_CHAR = {}
for i in range(10):
    ascii_val = ord('0') + i
    DECIMAL_TO_CHAR[ascii_val] = chr(ascii_val)
for i in range(26):
    ascii_val = ord('A') + i
    DECIMAL_TO_CHAR[ascii_val] = chr(ascii_val)

def decimal_to_binary(n, padding=7):
    """Converts a decimal number to binary string."""
    min_padding = max(len(bin(n)[2:]), padding)
    return bin(n)[2:].zfill(min_padding)

# FIXED PRIMES for the Prime-Power-Perfect-Sum (PPPS) System
FIXED_PRIMES = [5, 3, 2]

# --- 2. Prime-Power-Perfect-Sum (PPPS) Logic ---

def is_power_of_base(num, base):
    """Checks if a number is an exact power of the given base (base^E). Returns E or -1."""
    if num == 0:
        return -1 # Cannot be decomposed into a positive power, treat as failure
    if num == 1:
        return 0 # base^0 = 1
    
    # Check if log is an integer
    try:
        exponent = math.log(num, base)
        if abs(exponent - round(exponent)) < 1e-9: # Check for near-integer
            return int(round(exponent))
        return -1
    except ValueError:
        return -1

def decimal_to_perfect_summation(n, primes):
    """
    Finds the perfect partition N = 5^A + 3^B + 2^C.
    This uses a non-greedy search across all valid exponents A and B.
    
    Returns: (pbr_string, calculation_string)
    """
    p5, p3, p2 = primes
    
    # A. Search for perfect partition
    
    # Iterate through all possible exponents A for P=5
    max_A = int(math.log(n, p5)) if n >= p5 else 0
    
    # Iterate from max exponent down to 0, prioritizing smaller components
    for A in range(max_A, -1, -1):
        power_5 = p5 ** A
        remainder_A = n - power_5
        
        if remainder_A <= 0:
            if remainder_A == 0 and A >= 1: # Only 5^A = N (only if N is a power of 5)
                 return f"{A}00", f"N:{n} = {p5}^{A} + {p3}^0 + {p2}^0 = {power_5} + 1 + 1 = {power_5+2} (No Perfect Sum)"
            continue
            
        # Iterate through all possible exponents B for P=3
        max_B = int(math.log(remainder_A, p3)) if remainder_A >= p3 else 0
        
        for B in range(max_B, -1, -1):
            power_3 = p3 ** B
            remainder_B = remainder_A - power_3
            
            if remainder_B <= 0:
                # If remainder_B is exactly 0, check if 5^A + 3^B = N. If so, C= -1 (no P2 term)
                # But the user expects a 3-digit code (A, B, C). We must force 2^C.
                if remainder_B == 0:
                    # No 2^C term found in this branch. Continue searching.
                    continue 

            # Check if the final remainder R is a perfect power of P=2
            C = is_power_of_base(remainder_B, p2)
            
            if C != -1:
                # Perfect match found! N = 5^A + 3^B + 2^C
                pbr_str = f"{A}{B}{C}"
                power_2 = p2 ** C
                
                # Check that the sum is exactly N (it should be)
                total_sum = power_5 + power_3 + power_2
                
                calculation_str = (
                    f"N:{n} = {p5}^{A} + {p3}^{B} + {p2}^{C} = {power_5} + {power_3} + {power_2} = {total_sum} (Perfect Sum)"
                )
                return pbr_str, calculation_str

    # B. If no perfect partition found:
    return "XXX", f"N:{n} = (No Perfect Sum) - The number cannot be partitioned into $5^A + 3^B + 2^C$ with $A, B, C \ge 0$."


# --- 3. Main Execution and Chart Generation ---

def print_row(char, dec_val, binary_str, primes_str, pbr_str, math_str, header_format):
    """Helper function to format and print a single row."""
    display_char = char if char in DECIMAL_TO_CHAR.values() else f"({dec_val})"
    
    pbr_display = f"({pbr_str})_PPPS"
    
    print(
        header_format.format(display_char, dec_val, binary_str, primes_str, pbr_display, math_str)
    )

def generate_chart():
    """Generates the data and prints the formatted chart."""
    
    # Define table headers for 5 columns 
    header_format = "{:<4} | {:<7} | {:<12} | {:<50} | {:<18} | {:<250}"
    header = header_format.format("Ch", "ASCII", "Binary (B2)", "Fixed Primes & Exponent Rule", "PPPS (Exponents)", "Mathematical Check: N = $5^A + 3^B + 2^C$ (Perfect Partition Search)")
    
    header_length = len(header)
    
    # Print introductory information
    print("\n" + "=" * header_length)
    print("Prime-Power-Perfect-Sum System (PPPS) Chart ('0'-'Z')")
    print("Algorithm:")
    print("1. Goal: Find a perfect partition $N = 5^A + 3^B + 2^C$. Remainder must be 0.")
    print("2. Restriction REMOVED: Exponents A, B, C are found via **non-greedy search** (trying all combinations).")
    print("3. PPPS Code = (A B C) is the vector of exponents.")
    print("NOTE: For many numbers (like 51), a perfect partition does not exist.")
    print("=" * header_length + "\n")
    
    # --- Test Cases Confirmation ---
    print("--- Test Cases: N=13, N=50 to N=57 (Demonstrating Perfect Partition Search) ---")
    print(header)
    print("-" * header_length)
    
    # Test cases that previously showed repetition/problems (N=13, N=50, N=51)
    test_cases = [13] + list(range(50, 58))
    for dec_val in test_cases:
        # Use the fixed primes and calculate the PBR
        binary_str = decimal_to_binary(dec_val, padding=7)
        pbr_str, math_str = decimal_to_perfect_summation(dec_val, FIXED_PRIMES)
        
        # Format prime string for display
        primes_str = f"P_bases = {FIXED_PRIMES}"
        
        print_row("", dec_val, binary_str, primes_str, pbr_str, math_str, header_format)
        
    print("-" * header_length)
    print("\n--- Full ASCII Chart ('0'-'Z') using PPPS Logic ---")
    print(header)
    print("-" * header_length)
    
    # Generate and print rows for ASCII range
    all_ascii_values = sorted(DECIMAL_TO_CHAR.keys())
    
    for dec_val in all_ascii_values:
        char = DECIMAL_TO_CHAR[dec_val]
        
        # Column 3: Binary
        binary_str = decimal_to_binary(dec_val, padding=7)
        
        # Column 5, 6, & 7: PPCS Conversion and Calculation Math
        pbr_str, math_str = decimal_to_perfect_summation(dec_val, FIXED_PRIMES)
        
        primes_str = f"P_bases = {FIXED_PRIMES}"
        
        # Print the row
        print_row(char, dec_val, binary_str, primes_str, pbr_str, math_str, header_format)

if __name__ == "__main__":
    generate_chart()