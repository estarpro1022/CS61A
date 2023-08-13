# 1. Sequence

## 1.1 sequence unpacking

```python
>>> pairs = [[1, 2], [3, 3], [4, 5], [5, 5]]
>>> same_count = 0
>>> for x, y in pairs:
...     if x == y:
...         same_count += 1
... 
>>> same_count
2
```

This pattern of binding multiple names to multiple values in a fixed-length sequence is called *sequence unpacking*

## 1.2 Ranges

`range` 代表一系列连续整数，通常用于for循环的计数，也可以用`list`构造连续整数的集合

```python
>>> range(1, 5)
range(1, 5)
>>> list(range(1, 5))
[1, 2, 3, 4]
>>> list(range(5))
[0, 1, 2, 3, 4]
>>> for _ in range(3):
...     print("Kartone")
... 
Kartone
Kartone
Kartone
```

使用 `_` 作为变量名只是为了应对编译器，不会出现在后续表达式中

Length: ending value - starting value

## 1.3 List Comprehensions

利用原有list按照一定规则生成新的list，可以用if语句筛选

```python
>>> l = [1, 2, 3, 4]
>>> [x + 1 for x in l]
[2, 3, 4, 5]
>>> [x for x in l if x % 2 == 0]
[2, 4]
```

# 2. Data Abstraction

A *compound data* value that our programs can manipulate as **a single conceptual unit**, but which also has **two parts** that can be considered individually.

* 程序模块化
* 数据抽象

## 2.1 rational numbers

有理数可以表示为 `<numerator>/<denominator>`

- `rational(n, d)` returns the **rational number** with numerator `n` and denominator `d`.
- `numer(x)` returns the numerator of the rational number `x`.
- `denom(x)` returns the denominator of the rational number `x`.

针对有理数的操作：

```python
>>> def add_rationals(x, y):
        nx, dx = numer(x), denom(x)
        ny, dy = numer(y), denom(y)
        return rational(nx * dy + ny * dx, dx * dy)
>>> def mul_rationals(x, y):
        return rational(numer(x) * numer(y), denom(x) * denom(y))
>>> def print_rational(x):
        print(numer(x), '/', denom(x))
>>> def rationals_are_equal(x, y):
        return numer(x) * denom(y) == numer(y) * denom(x)
```

## 2.2 Pairs

任何把两个数据绑定起来的方式都叫pair，包含两元素的`list`是常见实现方式

`list`： 数据抽象的具体实现层面

```python
>>> from fractions import gcd
>>> def rational(n, d):
    	g = gcd(n, d)
        return [n//g, d//g]
>>> def numer(x):
        return x[0]
>>> def denom(x):
        return x[1]
```

list的下标从0开始，可以用`[]`取下标，也可以用`getitem`

```python
>>> l = [1, 2, 3]
>>> getitem(l, 0)
1
```

## 2.3 Abstraction Barriers(抽象壁垒)

数据抽象的核心思想就是定义一组操控数据的接口，使用时直接调用接口即可。

抽象壁垒就是将数据的表示(representation)和操作(operation)隔离开来，易于程序的维护和修改。当程序使用低层次的函数而不是使用高层次的函数时，抽象壁垒就会被打破

```python
# 正确使用方式
>>> def square_rational(x):
        return mul_rational(x, x)

# violate abstraction barrier
>>> def square_rational_violating_once(x):
        return rational(numer(x) * numer(x), denom(x) * denom(x))
```

## 2.4 Properties of Data

In general, we can express abstract data using a collection of **selectors** and **constructors**.

```python
>>> def pair(x, y):
        """Return a function that represents a pair."""
        def get(index):
            if index == 0:
                return x
            elif index == 1:
                return y
        return get
>>> def select(p, i):
        """Return the element at index i of pair p."""
        return p(i)
```

The practice of data abstraction allows us to switch data representation easily.
