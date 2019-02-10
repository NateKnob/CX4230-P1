from entities.society import Village
import time
import random
import numpy as np
import matplotlib.pyplot as plt


def main():
    random.seed(420)
    map = [[0 for _ in range(10)] for _ in range(10)]
    v = Village(30)
    map[3][4] = v
    villages = [v]

    popStats = [[] for v in villages]

    for _t in range(70):
        renderMap(map)

        for i, v in enumerate(villages):
            print(v.toString())
            # v.print_stats()
            v.update()
            print("-----------------------------------------------\n")
            popStats[i].append(v.getPopStats())
        time.sleep(0.1)

    for i, v in enumerate(villages):
        popStats[i] = np.asarray(popStats[i])
        print(popStats[i].shape)
    metrics = ["population", "adults", "farmers", "workers",
               "married", "food", "wood", "gold", "starve",
               "sick", "plague", "happiness"]
    plt.figure()
    for i in range(len(metrics)):
        plt.plot(popStats[0][:, i], label=metrics[i])
    plt.legend()
    plt.show()


def renderMap(map):
    for i in range(10):
        row = ""
        for j in range(10):
            if map[i][j] == 0:
                row += "[  ]"
            else:
                row += "[" + "{:02d}".format(map[i][j].countAdults()) + "]"
        print(row)
    print()


if __name__ == "__main__":
    main()
