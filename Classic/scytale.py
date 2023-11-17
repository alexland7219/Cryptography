#from string import ascii_lowercase as alf
from time import sleep

with open("CJueIAtO", "r") as ficher:
    st = ficher.read()

    for i in range(168, 169):
        if (len(st) % i == 0):
            print("n cols" + str(i))
            for j in range(0, len(st), i):
                print(st[j], end="")
            sleep(2)
            print("------------------------------")
            print(len(st))
