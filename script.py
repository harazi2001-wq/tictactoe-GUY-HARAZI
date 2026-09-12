from array import array

numbers= array("i",[1,2,3,4,5,6,7,8,9])

diary={"chris":1, "mike":2}
print(type(diary))

print(numbers)


for x in diary.items():
    print(x)

x = 10
y = 3
print(x // y)
print(x % y)

print('A', 'B', 'C', sep='-', end='!')
print('X')
x = 10
def my_func(y):
    x = 2
    return x * y
res = my_func(3)
print(res + x)
a = 1
b = 2
a, b = b, a + b
print(a, b)
b = b, a + b

s = 'a-b-c'
lst = s.split('-')
print('*'.join(lst))
s = 'Hello World'
print(s.find('o'))

data = []
try:
    with open('test.txt', 'w') as f:
        f.write('Hello\nWorld')
    with open('test.txt', 'r') as f:
        for line in f:
            data.append(line.strip().upper())
except FileNotFoundError:
    data.append('ERROR')
print(data)
def parse_numbers(text):
    result = []
    for item in text.split(','):
        try:
            result.append(int(item.strip()))
        except ValueError:
            result.append(0)
    return result
result = parse_numbers('10, abc, 20, , 30')
data = {'a': [1, 2], 'b': [3, 4]}
with open('output.txt', 'w') as f:
    for key in data:  # לולאה על מילון (מודול 5)
        values = data[key]  # רשימה (מודול 3)
        line = f'{key}:{sum(values)}\n'  # f-string (מודול 4)
        f.write(line)
print(line)
result = [x * 2 for x in range(1, 5) if x % 2 == 1]
print(result)

def func(word, sep=","):
    count = 0
    for char in word:
        count += 1
    for char in word:
        if char == sep:
            count += 1
    return count

print(func("ab,cd,ef,gh", ","))
def func():
    x = 0
    def inner():
        nonlocal x
        x += 1
        return x
    x = inner()
    x = inner()
    return x

print(func())

lst = [1, 5, 9, 13, 17]
print(lst[::2])
print(lst[1::2])
print(lst[::-1])
print(lst[-1::-2])
squares = [x**2 for x in range(5)]
print(squares)
nums = [0, 1, 2, 3]
result = list(filter(None, nums))
print(result)
class A:
    def __init__(self):
        self._x = 5
    @property
    def x(self):
        return self._x * 2

a = A()
print(a.x)

class A:
    def __call__(self):
        return "called"

a = A()
print(a())
for i, val in enumerate(['a', 'b', 'c']):
    print(i, val)
names = ['A', 'B', 'C']
scores = [80, 90, 70]

for n, s in zip(names, scores):
    print(n, s)


class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)
        return self

    def pop(self):
        return self._items.pop() if self._items else None

    def __len__(self):
        return len(self._items)


s = Stack()
s.push(1).push(2).push(3)
s.pop()
print(len(s), s.pop())

