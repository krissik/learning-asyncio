def fib(n):
    # Regular implementation
    fibs = []
    current = (0, 1)
    i = 0
    while i < n:
        tmp = current[0]
        fibs.append(tmp)
        current = (current[1], tmp + current[1])
        i += 1
    return fibs  # [::-1]  # Reverse order


def fibgen(n):
    # Generator
    # Return the first n fibonacci numbers
    current = (0, 1)
    i = 0
    while i < n:
        tmp = current[0]
        yield tmp
        current = (current[1], tmp + current[1])
        i += 1

for i in fibgen(100000):
    print(i)
