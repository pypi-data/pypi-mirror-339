import math

def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b): return a / b if b != 0 else "Error"
def sqrt(n): return math.sqrt(n)
def factorial(n): return math.factorial(n)
def power(base, exponent): return base ** exponent
def cbrt(n): return n ** (1/3)
def average(numbers): return sum(numbers) / len(numbers) if numbers else "Error"