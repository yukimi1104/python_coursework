#Lecture 1

#Press F9 to run a single line
#Press CTRL+ETNER to run the whole code (section)


print("Hello World")

#%% Documentation section

#!/usr/bin/python3


'''
prime.pl

Description: This program will output the first n numbers of prime numbers.
The user inputs the n and the program uses a mathematic function to calculate those prime numbers.

User-defined functions: None
Non-standard modules: 
    sh: Can call any external program as if it was a function
    
Procedure:
    1. Get the number of prime numbers to use from STDIN
    2. Iterate over all integers from 2 to an unknown number
    3. Test if the integer is a prime number, if so, add it to the list of prime numbers.
    4. When the list contains the numbers of prime numbers to produce end the iterations.
    5. Print all the elements in the list, one element per line

Input: n
Output: n prime numbers

Usage: ./prime.pl number_of_prime_numbers_to_report

Version: 1.00
Date: 2025-10-06
Name: Yiran Chen

'''


#%% Arithmetic 
#Question 1:
'''print(5/0)  #error
print(5//2)    #2
print(5%-2)    #-1;% gives the remainder that keeps the same sign as the divisor
print(-5%2)    #1
print(-5%-2 )  #-1
print(round(-3.6))  #-4
print(round(4.5)) #4
print(round(5.5)) #6
print(round(6.666,2))  #6.67'''

#Question 2:
'''round(int(4.6))=4
int(round(4.6)=5)'''

#Question 3:
'''int(-3.1)  #-3
import math
math.floor(-3.1) #-4
math.floor(3.1) #3
math.ceil(3.1) #4'''

#Question 4:
'''type(6.66) #float
int(6.66)
float(‘6.66’) 
int(‘6.66’) #error
Find a way of converting string ‘6.66’ to integer.
s = '6.66'
result = int(float(s))
print(result) '''

#%% String
#Question 1:
#len(5) will lead to error, because integer 5 has no elements and no length. 

#Question 2:
#len(str(len(‘len’))) 1

#Question 3:
'''a) You start with the variable my_string = "ATGC". What is the most
straightforward way of updating the content of my_string to
"ATGCXXX"? 
my_string = "ATGC"
my_string = my_string + "XXX"
print(my_string)
b) Starting with the variable my_string = "ATGC”. What is the simplest
way of updating it to "ATGCATGCATGCATGC"? (this should be solved in
a different way than the previous).
my_string="ATGC"
my_string = my_string * 4
print(my_string)
c) Calculate the length of the updated my_string variable.
print(len(my_string)) #16
d) Take the string "AAAAGGAAAAGGAAAA". Calculate the position of
the first GG.
my_string = "AAAAGGAAAAGGAAAA"
position = my_string.find("GG")
print(position)
#position = my_string.index("GG")
print(position) #4
e) *Then, find a way of calculating and printing the positions of all GGs
in the string. (You might need to check the documentation for this one).
count=my_string.count("GG")
import re
s = "ATGGCTGGGATG"
# 找到所有 "GG" 的起始位置（用 ?= 允许重叠匹配）
matches = re.finditer(r'(?=GG)', s)
# 提取并转换为 1-based 坐标
positions = [m.start() + 1 for m in matches]
print("GG found at positions:", positions)
print("Total number of GG:", len(positions))
f) Use the same string as in d). How many occurrences of AAAA are
there? AAA? AA? A? Do you understand why?
my_string = "AAAAGGAAAAGGAAAA"
print(my_string.count("AAAA"))
print(my_string.count("AAA"))
print(my_string.count("AA"))
print(my_string.count("A"))
# 3 4 6 12
g) Store the strings "AcgT" and "acGT" into two different variables, and
do a check on whether they contain the same letters. You can do this
with a basic comparison after doing a method-call on each of them. This
type of problem is common when working with sequence data, where
the sequences sometimes contain a mix of upper- and lower-case
letters.
seq1 = "AcgT"
seq2 = "acGT"
print(seq1.upper() == seq2.upper())
True
print(sorted(seq1.upper()) == sorted(seq2.upper()))
'''

#Question 4
name = "Karl"
surname = "Johansson"
print("My name is " + name + " " + surname)
print("My name is {} {}".format(name, surname))
print("My name is {1} {0}".format(name, surname))
print("My name is {0}{0} {1}".format(name, surname))
print("My name is {0}{0} {1}".format(name, surname[:5]))
#print("My name is {0}\t{1}".format(name, surname))
#print("My name is {1}\t{0}".format(name[:2], surname))


#Question 5
seq_1 = "AAATT "   # note: there is a space at the end
seq_2 = "CCCGG"
result = seq_1.strip() + seq_2
print(result)
print(f"{seq_1.strip()}{seq_2}")
result = "".join([seq_1.strip(), seq_2])
print(result)
result = seq_1.rstrip() + seq_2
print(result)

#Question 6
import random

seq = input("Enter a nucleotide sequence (A, C, G, T): ").upper()

index = random.randrange(len(seq))
nucleotides = ['A', 'C', 'G', 'T']
choices = [n for n in nucleotides if n != seq[index]]
new_base = random.choice(choices)

mutated_seq = seq[:index] + new_base + seq[index+1:]

print("Original sequence:", seq)
print("Mutated sequence :", mutated_seq)
print(f"Mutated position: {index}, {seq[index]} → {new_base}")


#%% Lecture 3 — Loops and Conditional Statements
# Tips: indentation defines code blocks in Python.

#%% 1) Print all multiples of 3 below 1000
print("1) Multiples of 3 below 1000:")
for i in range(0, 1000):
    if i % 3 == 0:
        print(i, end=" ")
print("\nDone.\n")

#%% 2) Print all multiples of 3, except those also multiples of 5, between 3000–4000
print("2) Multiples of 3 but not 5, between 3000 and 4000:")
for i in range(3000, 4001):
    if i % 3 == 0 and i % 5 != 0:
        print(i, end=" ")
print("\nDone.\n")

#%% 3) Fibonacci sequence
# Ask the user how many Fibonacci numbers to print (default = 10 to avoid blocking)
try:
    n = int(input("I want the number of FIBONACCI numbers: "))
except:
    n = 10

fib = []
a, b = 1, 1
for i in range(n):
    fib.append(a)
    a, b = b, a + b

print(f"The first {n} Fibonacci numbers are: {fib}")

#%% 4) Factorial of a user-entered number
import sys
try:
    s = input("Please enter a number: ")
    num = int(s)   # 转换成整数
    if num < 0:
        print("False enter (negative number)")
        sys.exit()
    # 如果输入为 0，阶乘结果应为 1
    if num == 0:
        print(1)
        sys.exit()
    result = 1
    for i in range(2, num + 1):
        result *= i
    print(result)
except ValueError:
    print("Please enter a valid integer.")


#%% 5) Print the first 1000 prime numbers (simple Sieve of Eratosthenes)
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
primes = []
num = 2  # start checking from 2

while len(primes) < 1000:
    if is_prime(num):
        primes.append(num)
    num += 1
for prime in primes:
    print(prime, end=' ')



















