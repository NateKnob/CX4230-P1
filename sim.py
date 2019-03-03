from entities.society import Village
import time
import random
import numpy as np
import matplotlib.pyplot as plt


def main():
    random.seed(20180210)
    map = [[0 for _ in range(10)] for _ in range(10)]
    v = Village(30)
    map[3][4] = v
    villages = [v]

    popStats = [[] for v in villages]

    for _t in range(200):
        # renderMap(map)
        print(_t)

        for i, v in enumerate(villages):
            # print(v.toString())
            # v.print_stats()
            # print("-----------------------------------------------\n")
            v.update()
            time.sleep(0.05)
            popStats[i].append(v.getPopStats())
            print(v.toString())
        # time.sleep(0.01)

    for i, v in enumerate(villages):
        popStats[i] = np.asarray(popStats[i])
        # print(popStats[i].shape)
    metrics = ["population", "adults", "farmers", "workers",
               "married", "food", "wood", "gold",
               "starve", "sick", "plague", "happiness"]
    plt.figure()
    for i in range(len(metrics)):
        label = metrics[i]
        if label != 'gold':
            plt.plot(popStats[0][:, i], label=label)
        else:
            plt.plot(popStats[0][:, i]/1000, label=label)
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
