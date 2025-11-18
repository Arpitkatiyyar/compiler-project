def check(a, b):
        if ((a > 0) and (b > 0)):
                    return True
        else:
                    return False

def main():
        x = 3
        y = (-1)
        if (check(x, y) or (x > 1)):
                    print("OK")
        else:
                    print("NOT OK")


if __name__ == "__main__":
    main()