import manipulation_math as mm

def read_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("wrong input.")


def main():
    print("which function you want to use?")
    print("1 - sum3power")
    print("2 - abs_sqrt-avg")

    choice = input("insert 1 or 2: ").strip()

    if choice == "1":
        a = read_number("enter first number: ")
        b = read_number("enter second number: ")
        c = read_number("enter third number: ")
        result = mm.sum3power(a, b, c)
        print("the answer is :", result)

    elif choice == "2":
        x = read_number("enter first number: ")
        y = read_number("enter second number: ")
        result = mm.abs_sqrt_avg(x, y)
        print("the answer is :", result)

    else:
        print("wrong input.")
if __name__ == "__main__":
    main()
