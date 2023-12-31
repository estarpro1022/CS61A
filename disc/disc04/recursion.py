def count_stairs(n):
    """ Returns number of ways to climb up N steps,
    moving either 1 or 2 steps.
    >>> count_stairs(1)
    1
    >>> count_stairs(3)
    3
    >>> count_stairs(5)
    8
    """
    if n == 1:
        return 1
    if n == 2:
        return 2
    return count_stairs(n - 1) + count_stairs(n - 2)

def count_k(n, k):
    """ Counts the number of paths up a flight of n stairs
    when taking up to and including k steps at a time.
    >>> count_k(3, 3) # 3, 2 + 1, 1 + 2, 1 + 1 + 1
    4
    >>> count_k(4, 4)
    8
    >>> count_k(10, 3)
    274
    >>> count_k(300, 1) # Only one step at a time
    1
    """
    if n == 0:
        return 1
    if n == 1:
        return 1
    if n < k:
        return count_k(n, n)
    
    sum = 0
    for i in range(1, k + 1):
        sum += count_k(n - i, k)
    return sum

def even_weighted(s):
    """
    >>> even_weighted([1, 2, 3, 4, 5])
    [0, 6, 20]
    """
    return [x * s[x] for x in range(len(s)) if x % 2 == 0]

def max_product(s):
    """ Returns maximum product generated by multiplication of nonsecutive elements. 
    >>> max_product([10, 5, 10, 5])
    100
    >>> max_product([4, 2, 6, 8])
    32
    >>> max_product([10,3,1,9,2]) # 10 * 9
    90
    >>> max_product([5,10,5,10,5]) # 5 * 5 * 5
    125
    >>> max_product([])
    1
    """
    length = len(s)
    if length == 0:
        return 1
    if length == 1:
        return s[0]
    if length == 2:
        return max(s[0], s[1])
    first = s[0] * max_product(s[2:])
    second = s[1] * max_product(s[3:])
    return max(first, second)

def max_product_official(s):
    if len(s) == 0:
        return 1
    # select first item or not
    return max(s[0] * max_product_official(s[2:]), max_product_official(s[1:]))