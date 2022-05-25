#1
x = int(input('Введите число: '))
def fact(x):
    if x == 0:
        return 1
    else:
        return x * fact(x - 1)
print('Ответ: ', fact(x))

#2
lst = list(map(int, input('Введите список: ').split()))
def filter_even(li):
    ans = filter(lambda x: (x % 2 == 0), li)
    return ans
print('Ответ: ', *filter_even(lst))

#3
lst = list(map(int, input('Введите список: ').split()))
def square(li):
  ans = map(lambda x: x ** 2, li)
  return ans
print('Ответ: ', *square(lst))

#4
lst, n = input('Введите список и элемент: ').split()
n = int(n)
lst = list(map(int, lst[1:-2].split(',')))
def bin_search(li, element):
    start = 0
    end = len(li)
    middle = 0
    step = 0
    while start <= end and start < len(li):
        middle = (start + end) // 2
        if element == li[middle]:
            return middle
        if element < li[middle]:
            end = middle - 1
        else:
            start = middle + 1
    return -1
print('Ответ: ', bin_search(lst, n))

#5
import string
s = input('Введите строку: ')
s1 = s.lower().replace(' ', '')
for char in s1:
    if char in string.punctuation:
        s1 = s1.replace(char, '')
def is_palindrome(string):
    for i in range(len(string) // 2):
        if string[i] != string[-1 - i]:
            return 'NO'
    return 'YES'
print(is_palindrome(s1))

#6
def calculate(file):
    with open(file) as file1:
        ans = []
        for line in file1:
            s = line.split()
            if s[0] == '+':
                ans.append(int(s[1]) + int(s[2]))
            elif s[0] == '-':
                ans.append(int(s[1]) - int(s[2]))
            elif s[0] == '*':
                ans.append(int(s[1]) * int(s[2]))
            elif s[0] == '//':
                ans.append(int(s[1]) // int(s[2]))
            elif s[0] == '%':
                ans.append(int(s[1]) % int(s[2]))
            elif s[0] == '**':
                ans.append(int(s[1]) ** int(s[2]))
    return ','.join(ans)

#7
def substring_slice(path2file_1,path2file_2):
    with open(path2file_1, 'r') as file1, open(path2file_2, 'r') as file2:
        ans = []
        for line1, line2 in zip(file1, file2):
            start, end = map(int, line2.split())
            if start == end:
                ans.append(line1[start])
            else:
                ans.append(line1[start : end + 1])
    return ' '.join(ans)

#8
import json
def decode_ch(string):
    periodic_table = json.load(open('periodic_table.json', 'r', encoding='utf-8'))
    ans = ''
    curr_string = ''
    for elem in string:
        if elem.isupper():
            if not curr_string:
                curr_string += elem
            else:
                ans += periodic_table[curr_string]
                curr_string = elem
        else:
            curr_string += elem
    ans += periodic_table[curr_string]
    return ans
print(decode_ch('NOTiFICaTiON'))

#9
class Student(object):
    def __init__(self, name, surname, grades = [3, 4, 5]):
        self.name = name
        self.surname = surname
        self.fullname = name + ' ' + surname
        self.grades = grades
    def greeting(self):
        print('Hello, I am Student')
    def mean_grade(self):
        return sum(self.grades) / len(self.grades)
    def is_otlichnik(self):
        if self.mean_grade() >= 4.5:
            return 'YES'
        else:
            return 'NO'
    def __add__(self, other):
        return self.name + ' is friends with ' + other.name
    def __str__(self):
        return self.fullname

#10
class MyError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return'Ошибка MyError, {0}'.format(self.msg)
while True:
    try:
        n = int(input('Введите целое положительное число, меньшее 10: '))
        if n >= 10:
            raise MyError('Вы ввели число, большее или равное 10')
        elif n < 0:
            raise MyError('Вы ввели отрицательное число')
    except MyError as e:
        print(e)
    else:
        print('Вы ввели корректное число!')
        break
