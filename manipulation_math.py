import math

def sum3power(a,b,c):
    return (a**3) + (b**3) + (c**3)

def abs_sqrt_avg(x,y):
    return (math.sqrt(abs(x)) + math.sqrt(abs(y))) / 2

def main():
    print("sum3power(2, 3, 4) =", sum3power(2, 3, 4))
    print("avg_sqrt_abs(16, -9) =", abs_sqrt_avg(16, -9))
if __name__ == '__main__':
    main()