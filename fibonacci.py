def fib_recursive(amount) -> int:
    if amount <= 0:
        raise ValueError("Must be a positive integer.")
    elif amount == 1:
        return 0
    elif amount == 2:
        return 1
    else:
        return fib_recursive(amount - 1) + fib_recursive(amount - 2)


print(fib_recursive(1))  # Output: 0 (0)
print(fib_recursive(2))  # Output: 1 (0, 1)
print(fib_recursive(5))  # Output: 3 (0, 1, 1, 2, 3)
print(fib_recursive(10))  # Output: 34 (0, 1, 1, 2, 3, 5, 8, 13, 21, 34)
