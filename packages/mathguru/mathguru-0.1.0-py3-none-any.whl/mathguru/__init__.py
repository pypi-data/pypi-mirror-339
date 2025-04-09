import math
import numpy as np

# Arithmetic functions
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b): return a / b if b != 0 else float('inf')
def floor_divide(a, b): return a // b
def modulo(a, b): return a % b
def power(a, b): return a ** b

# Trigonometry
def sin(x): return math.sin(x)
def cos(x): return math.cos(x)
def tan(x): return math.tan(x)
def asin(x): return math.asin(x)
def acos(x): return math.acos(x)
def atan(x): return math.atan(x)
def degrees(x): return math.degrees(x)
def radians(x): return math.radians(x)

# Logarithmic & exponential
def log(x, base=math.e): return math.log(x, base)
def log10(x): return math.log10(x)
def log2(x): return math.log2(x)
def exp(x): return math.exp(x)

# Rounding & absolute
def floor(x): return math.floor(x)
def ceil(x): return math.ceil(x)
def round_val(x, ndigits=0): return round(x, ndigits)
def abs_val(x): return abs(x)

# Roots
def sqrt(x): return math.sqrt(x)
def cbrt(x): return np.cbrt(x)

# Statistical (custom)
def mean(arr): return sum(arr) / len(arr) if arr else 0
def median(arr): return np.median(arr)
def mode(arr): return max(set(arr), key=arr.count)
def variance(arr): return np.var(arr)
def std_dev(arr): return np.std(arr)

# Number properties
def is_even(x): return x % 2 == 0
def is_odd(x): return x % 2 != 0
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

# Combinatorics
def factorial(n): return math.factorial(n)
def comb(n, k): return math.comb(n, k)
def perm(n, k): return math.perm(n, k)

# Geometry
def area_circle(r): return math.pi * r * r
def circumference_circle(r): return 2 * math.pi * r
def area_triangle(b, h): return 0.5 * b * h
def area_rectangle(l, w): return l * w

# Conversions
def to_binary(n): return bin(n)[2:]
def to_hex(n): return hex(n)[2:]
def to_octal(n): return oct(n)[2:]

# Random useful ones
def gcd(a, b): return math.gcd(a, b)
def lcm(a, b): return abs(a * b) // math.gcd(a, b)
def clamp(val, min_val, max_val): return max(min(val, max_val), min_val)

# Constants
PI = math.pi
E = math.e
TAU = math.tau
INF = float('inf')
NAN = float('nan')
