from fractions import Fraction
from math import factorial, isqrt


def is_prime(n: int) -> bool:
    if n < 2:
        return False

    for divisor in range(2, isqrt(n) + 1):
        if n % divisor == 0:
            return False

    return True


print(f"{'n':>3}  {'n! / (n/3)^2':>25}  {'Inferred prime?':>15}  {'Actually prime?':>15}  Match?")
print("-" * 75)

mismatches = []

for n in range(5, 101):
    expression = Fraction(factorial(n), 1) / Fraction(n, 3) ** 2

    # A non-integer result is inferred to mean prime.
    inferred_prime = expression.denominator != 1
    actual_prime = is_prime(n)
    matches = inferred_prime == actual_prime

    print(
        f"{n:>3}  {str(expression):>25}  "
        f"{str(inferred_prime):>15}  {str(actual_prime):>15}  "
        f"{'Yes' if matches else 'NO'}"
    )

    if not matches:
        mismatches.append(n)

print("\nMismatches:", mismatches if mismatches else "None")