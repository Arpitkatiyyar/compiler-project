def factorial(n):
        f = 1
        for i in range(1, (n + 1), 1):
                    f = (f + (f * (i - 1)))
        return f

def fibonacci(n):
        a = 0
        b = 1
        temp = 0
        for i in range(1, (n + 1), 1):
                    temp = (a + b)
                    a = b
                    b = temp
        return a

def sumSquares(n):
        s = 0
        for i in range(1, (n + 1), 1):
                    s = (s + (i * i))
        return s

def compute(x, y, z):
        fact = factorial(x)
        fib = fibonacci(y)
        sq = sumSquares(z)
        result = ((fact + fib) + sq)
        return result

def main():
        x = 0
        y = 0
        z = 0
        print("Enter x: ", end='')
        x = int(input())
        print("Enter y: ", end='')
        y = int(input())
        print("Enter z: ", end='')
        z = int(input())
        print("Processing...")
        output = compute(x, y, z)
        print("Final Output = ", output)


if __name__ == "__main__":
    main()