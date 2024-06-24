from operator import add, sub

def a_plus_abs_b(a, b):
    """Return a+abs(b), but without calling abs.

    >>> a_plus_abs_b(2, 3)
    5
    >>> a_plus_abs_b(2, -3)
    5
    >>> a_plus_abs_b(-1, 4)
    3
    >>> a_plus_abs_b(-1, -4)
    3
    """
    if b < 0:
        f = lambda a,b: a - b
    else:
        f = lambda a,b: a + b
    return f(a, b)

# !!!
def a_plus_abs_b_syntax_check():
    """Check that you didn't change the return statement of a_plus_abs_b.

    >>> # You aren't expected to understand the code of this test.
    >>> import inspect, re
    >>> re.findall(r'^\s*(return .*)', inspect.getsource(a_plus_abs_b), re.M)
    ['return f(a, b)']
    """
    # You don't need to edit this function. It's just here to check your work.

# 我这种做法虽然正确，但是不符合作业预期
# def two_of_three(i, j, k):
#     """Return m*m + n*n, where m and n are the two smallest members of the
#     positive numbers i, j, and k.
#
#     >>> two_of_three(1, 2, 3)
#     5
#     >>> two_of_three(5, 3, 1)
#     10
#     >>> two_of_three(10, 2, 8)
#     68
#     >>> two_of_three(5, 5, 5)
#     50
#     """
#     min_num = min(i, j, k)
#     if min_num == i:
#         min_num_2 = min(j, k)
#     elif min_num == j:
#         min_num_2 = min(i, k)
#     else:
#         min_num_2 = min(i, j)
#     return min_num**2 + min_num_2**2


# !!!

def two_of_three(i, j, k):
    """Return m*m + n*n, where m and n are the two smallest members of the
    positive numbers i, j, and k.

    >>> two_of_three(1, 2, 3)
    5
    >>> two_of_three(5, 3, 1)
    10
    >>> two_of_three(10, 2, 8)
    68
    >>> two_of_three(5, 5, 5)
    50
    """
    return sum(sorted([i**2,j**2,k**2])[:2])

def two_of_three_syntax_check():
    """Check that your two_of_three code consists of nothing but a return statement.

    >>> # You aren't expected to understand the code of this test.
    >>> import inspect, ast
    >>> [type(x).__name__ for x in ast.parse(inspect.getsource(two_of_three)).body[0].body]
    ['Expr', 'Return']
    """
    # You don't need to edit this function. It's just here to check your work.


def largest_factor(n):
    """Return the largest factor of n that is smaller than n.

    >>> largest_factor(15) # factors are 1, 3, 5
    5
    >>> largest_factor(80) # factors are 1, 2, 4, 5, 8, 10, 16, 20, 40
    40
    >>> largest_factor(13) # factor is 1 since 13 is prime
    1
    """
    "*** YOUR CODE HERE ***"
    # 1
    # 2:1
    # 3:1
    # 4:2
    # 5:1
    # 6:2,3
    # 7:1
    # 8:1,2,4
    # 9:1,3
    # 10:1,2,5
    # 11:1
    # 12:1,2,3,46
    # 13:1
    # if n % 2
#     质数怎么通过方法判断
# 通过去取余比自己小的数，如果有==0的情况，说明不是质数，则将该因数放入列表，后续从列表中拿出最大的数
    if n == 1:
        return None
    if n == 2:
        return 1
    num = 2
    factor_list = [1,]
    while num < n:
        if n % num == 0:
            factor_list.append(num)
        num += 1

    return max(factor_list)

def hailstone(n):
    """Print the hailstone sequence starting at n and return its
    length.

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
    >>> b = hailstone(1)
    1
    >>> b
    1
    """
    "*** YOUR CODE HERE ***"
    length = 0
    if n == 1:
        print(n)
        return 1
    while n != 1:
        print(n)
        length += 1
        if n % 2 == 0:
            n = n // 2
        else:
            n = n * 3 + 1
    print(n)
    return length + 1