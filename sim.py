from entities.humans import Person, Farmer
from entities.society import Village
import time
import random
import numpy as np
import matplotlib.pyplot as plt

metrics = ["old", "young", "adult", "sickos", "total", "food", "births", "deaths", "illDeaths"]

def main():
    random.seed(420)

    map = [[0 for i in range(10)] for i in range(10)]

    v = Village(30)
    map[3][4] = v
    vs = [v]


    popStats = [[] for v in vs]

    for i in range(70):
        renderMap(map)
        for vi, v in enumerate(vs):
            v.work()
            print(v.toString())
            popStats[vi].append(v.getPopStats())
        time.sleep(0.1)

    for vi, v in enumerate(vs):
        popStats[vi] = np.asarray(popStats[vi])
        print(popStats[vi].shape)

    plt.figure()
    for i in range(9):
        plt.plot(popStats[vi][:, i], label=metrics[i])
    plt.legend()
    plt.show()

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
