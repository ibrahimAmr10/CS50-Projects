from cs50 import get_float

change = 0
coin = 0
while change <= 0:
    change = get_float("Change: ")


def reducer(ce):
    global change
    global coin
    while (change >= ce):
        change = round(change - ce, 10)
        coin += 1


reducer(0.25)
reducer(0.10)
reducer(0.05)
reducer(0.01)


print(coin)
