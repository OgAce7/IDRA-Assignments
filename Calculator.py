def main():
    print("=== Arithmetic Operations Calculator ===")
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
    except ValueError:
        print("Invalid input! Please enter numeric values only.")
        return
    print("\n--- Results ---")
    addition = num1 + num2
    print(f"Addition ({num1} + {num2})          = {addition}")
    subtraction = num1 - num2
    print(f"Subtraction ({num1} - {num2})       = {subtraction}")
    multiplication = num1 * num2
    print(f"Multiplication ({num1} * {num2})    = {multiplication}")
    if num2 != 0:
        division = num1 / num2
        print(f"Division ({num1} / {num2})          = {division}")
    else:
        print("Division ({num1} / {num2})          = Error (Division by zero)")
    if num2 != 0:
        floor_division = num1 // num2
        print(f"Floor Division ({num1} // {num2})    = {floor_division}")
    else:
        print("Floor Division ({num1} // {num2})    = Error (Division by zero)")
    if num2 != 0:
        modulus = num1 % num2
        print(f"Modulus ({num1} % {num2})          = {modulus}")
    else:
        print("Modulus ({num1} % {num2})          = Error (Division by zero)")
    exponentiation = num1 ** num2
    print(f"Exponentiation ({num1} ** {num2})    = {exponentiation}")
if __name__ == "__main__":
    main()