def main():
        x = 10
        y = 5
        if (x > 0):
                    print("x is positive")
                    if (y > 0):
                                    print("y is also positive")
                                    if (x > y):
                                                        print("x is greater than y")
                                    else:
                                                        print("y is greater or equal to x")
                    else:
                                    print("y is non-positive")
        else:
                    print("x is non-positive")
        return 0


if __name__ == "__main__":
    main()