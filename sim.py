from entities.humans import Person, Farmer
from entities.society import Village
import time
import random

def main():
    random.seed(420)

    map = [[0 for i in range(10)] for i in range(10)]

    v = Village(12)
    map[3][4] = v
    vs = [v]



    for i in range(200):
        renderMap(map)
        for v in vs:
            v.work()
            print(v.toString())
        time.sleep(0.1)

def renderMap(map):
    for i in range(10):
        row = ""
        for j in range(10):
            if map[i][j] == 0:
                row += "[  ]"
            else:
                row += "[" + "{:02d}".format(map[i][j].countAdults())+ "]"
        print(row)
    print()


if __name__ == "__main__":
    main()
