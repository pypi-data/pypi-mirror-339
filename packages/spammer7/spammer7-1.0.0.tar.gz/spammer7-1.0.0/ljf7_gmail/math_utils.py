def fib(n):
    if n < 2:
        return n
    else:
        return fib(n-1) + fib(n-2)


def fact(n):
    if n < 2:
        return n
    else:
        return n * fact(n-1)
