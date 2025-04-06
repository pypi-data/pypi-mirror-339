import math
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

options = {
    0: "Exit",
    1: "Add",
    2: "Subtract",
    3: "Multiply",
    4: "Divide",
    5: "Percentage",
    6: "Square Root",
    7: "Power",
    8: "Matrix Addition",
    9: "Matrix Subtraction",
}

def addition():
    addition_number = int(input(Fore.CYAN + "How many numbers to add: "))
    add_list = []

    for i in range(addition_number):
        number = int(input(Fore.CYAN + "Enter the number you want to add: "))
        add_list.append(number)

    print(Fore.GREEN + f"Addition of the numbers {add_list} is {sum(add_list)}")

def subtract():
    a = int(input(Fore.CYAN + "Value of a: "))
    b = int(input(Fore.CYAN + "Value of b: "))
    print(Fore.GREEN + f"Result: {a - b}")

def multiply():
    numbers = int(input(Fore.CYAN + "How many numbers to multiply: "))
    result = 1
    for _ in range(numbers):
        num = int(input(Fore.CYAN + "Enter the number: "))
        result *= num
    print(Fore.GREEN + f"Result: {result}")

def divide():
    a = int(input(Fore.CYAN + "Value of a: "))
    b = int(input(Fore.CYAN + "Value of b: "))
    if b == 0:
        print(Fore.RED + "Division by zero is not allowed.")
    else:
        print(Fore.GREEN + f"Result: {a / b}")

def percentage():
    a = float(input(Fore.CYAN + "Enter the total: "))
    b = float(input(Fore.CYAN + "Enter the value: "))
    print(Fore.GREEN + f"Result: {(b / a) * 100}%")

def square_root():
    a = float(input(Fore.CYAN + "Enter the number: "))
    print(Fore.GREEN + f"Result: {math.sqrt(a)}")

def power():
    a = int(input(Fore.CYAN + "Base: "))
    b = int(input(Fore.CYAN + "Exponent: "))
    print(Fore.GREEN + f"Result: {a ** b}")

def matrix_addition():
    try:
        rows = int(input(Fore.CYAN + "Enter number of rows: "))
        cols = int(input(Fore.CYAN + "Enter number of columns: "))
        if rows <= 0 or cols <= 0:
            raise ValueError("Dimensions must be positive integers.")

        def get_matrix(rows, cols, name="Matrix"):
            print(Fore.YELLOW + f"\nEnter elements of {name} (row by row):")
            matrix = []
            for i in range(rows):
                while True:
                    try:
                        row = input(Fore.CYAN + f"Row {i + 1}: ").strip().split()
                        if len(row) != cols:
                            raise ValueError(f"Expected {cols} elements.")
                        matrix.append([int(x) for x in row])
                        break
                    except ValueError as e:
                        print(Fore.RED + f"Invalid input: {e}. Try again.")
            return matrix

        def add_matrices(m1, m2):
            return [[m1[i][j] + m2[i][j] for j in range(cols)] for i in range(rows)]

        matrix1 = get_matrix(rows, cols, "Matrix 1")
        matrix2 = get_matrix(rows, cols, "Matrix 2")
        result = add_matrices(matrix1, matrix2)

        print(Fore.GREEN + "\nResult Matrix:")
        for row in result:
            for num in row:
                print(Fore.GREEN + str(num), end=" ")
            print()

    except ValueError as e:
        print(Fore.RED + f"Error: {e}")

def matrix_subtraction():
    try:
        rows = int(input(Fore.CYAN + "Enter number of rows: "))
        cols = int(input(Fore.CYAN + "Enter number of columns: "))
        if rows <= 0 or cols <= 0:
            raise ValueError("Dimensions must be positive integers.")

        def get_matrix(rows, cols, name="Matrix"):
            print(Fore.YELLOW + f"\nEnter elements of {name} (row by row):")
            matrix = []
            for i in range(rows):
                while True:
                    try:
                        row = input(Fore.CYAN + f"Row {i + 1}: ").strip().split()
                        if len(row) != cols:
                            raise ValueError(f"Expected {cols} elements.")
                        matrix.append([int(x) for x in row])
                        break
                    except ValueError as e:
                        print(Fore.RED + f"Invalid input: {e}. Try again.")
            return matrix

        def subtract_matrices(m1, m2):
            return [[m1[i][j] - m2[i][j] for j in range(cols)] for i in range(rows)]

        matrix1 = get_matrix(rows, cols, "Matrix 1")
        matrix2 = get_matrix(rows, cols, "Matrix 2")
        result = subtract_matrices(matrix1, matrix2)

        print(Fore.GREEN + "\nResult Matrix:")
        for row in result:
            for num in row:
                print(Fore.GREEN + str(num), end=" ")
            print()

    except ValueError as e:
        print(Fore.RED + f"Error: {e}")


def main():
    while True:
        print(Fore.YELLOW + "\n--- Calculator Menu ---")
        for key in options:
            print(Fore.YELLOW + f"{key} - {options[key]}")

        try:
            option = int(input(Fore.CYAN + "\nChoose an option (press 0 to exit): "))
        except ValueError:
            print(Fore.RED + "Please type correct input")
            continue

        if option == 0:
            print(Fore.MAGENTA + "Exiting the calculator, good bye.")
            break

        if option in options:
            print(Fore.BLUE + f"You have chosen to {options[option]}")

            if option == 1:
                addition()
            elif option == 2:
                subtract()
            elif option == 3:
                multiply()
            elif option == 4:
                divide()
            elif option == 5:
                percentage()
            elif option == 6:
                square_root()
            elif option == 7:
                power()
            elif option == 8:
                matrix_addition()
            elif option == 9:
                matrix_subtraction()
        else:
            print(Fore.RED + "Invalid input, please choose correct option.")

if __name__ == "__main__":
    main()
