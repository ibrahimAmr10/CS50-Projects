from cs50 import get_int
n = 0
while n < 1 or n > 8:
    n = get_int("Height: ")
for j in range(n):
    print(" " * (n-1-j), end="")
    print("#" * (j+1))
