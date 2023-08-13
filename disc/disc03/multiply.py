def mul(m, n):
    """Takes two positive integers and return m * n with a recursive method.
    >>> mul(3, 2)
    6
    >>> mul(0, 2)
    0
    >>> mul(8, 1)
    8
    >>> mul(512, 5)
    2560
    """
    a, b = max(m, n), min(m, n)
    return mul_helper(a, b)

def mul_helper(a, b):
    """argument: a >= b"""
    if b == 0:
        return 0
    if b == 1:
        return a
    return mul_helper(a, b - 1) + a

def is_prime(n):
    """Return True if n is prime and False otherwise. Assume n > 1
    >>> is_prime(522)
    False
    >>> is_prime(9)
    False
    >>> is_prime(11)
    True
    >>> is_prime(2)
    True
    >>> is_prime(3)
    True
    """
    def divided(m):
        if m == 1:
            return False
        if n % m == 0:
            return True
        return divided(m - 1)
    return not divided(n - 1)

def hailstone(n):
    """divides n by 2 if n is even, or muls n by three and adds one
    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    """
    print(n)
    if n == 1:
        return 1
    if n % 2 == 0:
        return hailstone(n // 2) + 1
    return hailstone(n * 3 + 1) + 1

def len(n):
    if n < 10:
        return 1
    return len(n // 10) + 1

def merge(n1, n2):
    """Returns merger of two numbers with all the digits in decreasing order
    >>> merge(3, 2)
    32
    >>> merge(51, 6)
    651
    >>> merge(553211, 999871)
    999875532111
    >>> merge(21, 31)
    3211
    """
    if n1 == 0:
        return n2
    if n2 == 0:
        return n1
    len1, len2 = len(n1), len(n2)
    pow_ten_1, pow_ten_2 = 10 ** (len1 - 1), 10 ** (len2 - 1)
    first1, first2 = n1 // pow_ten_1, n2 // pow_ten_2

    if first1 > first2:
        return first1 * 10 ** (len1 + len2 - 1) + merge(n1 % pow_ten_1, n2)
    return first2 * 10 ** (len1 + len2 - 1) + merge(n1, n2 % pow_ten_2)

def merge_official(n1, n2):
    """construct from low digit to high.

    >>> merge_official(3, 1)
    31
    >>> merge_official(52, 71)
    7521
    """  
    if n1 == 0:
        return n2
    if n2 == 0:
        return n1
    last1, last2 = n1 % 10, n2 % 10
    if last1 < last2:
        return merge_official(n1 // 10, n2) * 10 + last1
    return merge_official(n1, n2 // 10) * 10 + last2

