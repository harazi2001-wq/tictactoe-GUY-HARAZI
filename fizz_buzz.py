def fizz_buzz(num):
    if num % 3 == 0 and num % 5 == 0:
        return "FizzBuzz"
    elif num % 3 == 0:
        return "Fizz"
    elif num % 5 == 0:
        return "Buzz"
    else:
        return num
def main():
    print("what is fizz_buzz")
    num = int(input("Enter a number: "))
    print(fizz_buzz(num))

main()

