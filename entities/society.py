import random
from collections import Counter
from entities.humans import *
from entities.occupation import *
import numpy as np
import time

min_food = 12
good_food = 20

vsize = 12
all_coords = [(a, b) for a in range(vsize) for b in range(vsize)]
n_coords = [(a,b) for a in [-1, 0, 1] for b in [-1, 0, 1]]

collapseChance = 0.75

caps = {"wood": 1000}

class Village:
    def __init__(self, size=random.randint(10, 20)):
        self.grid = np.empty((12,12), dtype=object)
        self.grid[:,:] = -1
        self.population = [PersonFactory.makeRandomPerson() for _ in range(size)]
        np.random.shuffle(all_coords)
        for i, (x, y) in enumerate(all_coords[:size]):
            self.grid[x,y] = self.population[i]

        self.area = np.count_nonzero(self.grid == None)
        self.crowding = 0
        self.foodNeed = 3
        self.wealth = Counter({"food": size * 100, "wood": size * 100, "gold": 0})
        self.metrics = Counter()
        self.happiness = 70

    def _clean(self, reason):
        before = len(self.population)
        self.population = []
        for (x,y) in all_coords:
            op = self.grid[x,y]
            if type(op) == Person:
                if op.isAlive():
                    self.population.append(op)
                else:
                    del op
                    self.grid[x,y] = None
        #self.population = [person for person in self.grid if type(person) == Person and person.isAlive()]
        self.metrics["deaths_" + reason] += (before - len(self.population))
        #time.sleep(5)
        self.area = np.count_nonzero(self.grid == None)
        self.crowding = np.clip(40-self.area, 0, 20)/20

        # for product in caps:
        #     self.wealth[product] = min(self.wealth[product], caps[product])


    def _work(self):
        for person in self.population:
            person.work(self)

    def _feed(self):
        needed_food = len(self.population) * good_food
        if self.wealth['food'] >= needed_food:
            if self.wealth['food'] >= 5 * needed_food:
                self.foodNeed -= 1
                self.foodNeed = max(self.foodNeed, 1)
            else:
                self.foodNeed += 1
                self.foodNeed = min(self.foodNeed, 5)
            ration = good_food
            self.happiness += 2
        else:
            ration = self.wealth['food'] // len(self.population)
            self.happiness -= 5
            self.foodNeed += 2
            self.foodNeed = min(self.foodNeed, 5)

        for person in self.population:
            actual_food = max(ration, min_food) + random.randint(-1, 1)
            if self.wealth['food'] < actual_food:
                person.die()
            else:
                self.wealth['food'] -= actual_food
        self._clean("starve")

    def _disease(self):
        for person in self.population:
            person.disease(self)
        self._clean("plague")

    def _mingle(self):
        bm = self.getBachelors()
        bf = self.getBachelorettes()
        for i in range(min(len(bm), len(bf))):
            bm[i].marry(bf[i])
            bf[i].marry(bm[i])

    def _procreate(self):
        births = 0
        for person in self.population:
            if person.procreate():
                births += 1
                pi = np.where(self.grid == person)
                if len(pi[0]) > 0:
                    px, py = pi[0][0], pi[1][0]
                    np.random.shuffle(n_coords)
                    for (nx, ny) in n_coords:
                        try:
                            if self.grid[px+nx, py+ny] == None:
                                self.grid[px+nx, py+ny] = Person()
                                break
                        except IndexError as e:
                            pass
        # for _ in range(births):
        #     self.population.append(Person())

    def _build(self):
        if self.area > 0:
            ii = np.where(self.grid == None)
            for i in range(len(ii[0])):
                if random.random() < collapseChance:
                    px, py = ii[0][i], ii[1][i]
                    if len(self.getNeighborsFromCoords(px, py)) == 0:
                        self.grid[px, py] = -1



        if self.area < 20:
            newSpaces = self.wealth['wood'] // 100
            for i in range(min(newSpaces, 6)):
                if len(self.population) > 0:
                    adjs = self.getAdjacents(np.random.choice(self.population))
                    for a in adjs:
                        if a[2] == -1:
                            self.grid[a[0], a[1]] = None
                            self.wealth['wood'] -= 100
                            break
        else:
            self.wealth['gold'] += self.wealth['wood'] // 2
            self.wealth['wood'] -= self.wealth['wood'] // 2

    def update(self):
        self._work()
        self._feed()
        self._disease()
        self._mingle()
        self._procreate()
        self._build()
        self.happiness = min(max(0, self.happiness), 100)

    def print_stats(self):
        print("Population:", len(self.population))
        print("Area     :", self.area)
        print("Food Need:", self.foodNeed)
        print("Adults   :", self.countAdults())
        print("\tFarmers  :", len([p for p in self.population if type(p.occupation) == Farmer]))
        print("\tWorkers  :", len([p for p in self.population if type(p.occupation) == Worker]))
        print("Marrieds :", len(self.getMarrieds()))
        print("Sick     :", len(self.getSickos()))
        print("Starved  :", self.metrics["deaths_starve"])
        print("Plague   :", self.metrics["deaths_plague"])
        print("Food     :", self.wealth["food"])
        print("Wood     :", self.wealth["wood"])
        print("Gold     :", self.wealth["gold"])
        print("Happiness:", self.happiness)

    def getPopStats(self):
        # metrics = ["population", "adults", "farmers", "workers",
        #            "married", "food", "wood", "gold", "starve",
        #            "sick", "plague", "happiness"]
        return [len(self.population), self.countAdults(),
                len([p for p in self.population if type(p.occupation) == Farmer]),
                len([p for p in self.population if type(p.occupation) == Worker]), len(self.getMarrieds()),
                self.wealth["food"] // 100, self.wealth["wood"] // 100,
                self.wealth["gold"], self.metrics["deaths_starve"],
                len(self.getSickos()), self.metrics["deaths_plague"], self.happiness]

    def getAdjacents(self, obj):
        ns = []
        pi = np.where(self.grid == obj)
        if len(pi[0]) > 0:
            px, py = pi[0][0], pi[1][0]
            np.random.shuffle(n_coords)
            for (nx, ny) in n_coords:
                if (px+nx > -1 and px+nx < vsize and py+ny > -1 and py+ny < vsize):
                    ns.append((px+nx, py+ny, self.grid[px+nx, py+ny]))

        return ns

    def getAdjacentsFromCoords(self, px, py):
        ns = []
        np.random.shuffle(n_coords)
        for (nx, ny) in n_coords:
            if (px+nx > -1 and px+nx < vsize and py+ny > -1 and py+ny < vsize):
                ns.append((px+nx, py+ny, self.grid[px+nx, py+ny]))
        return ns


    def getNeighbors(self, obj):
        return [n for n in self.getAdjacents(obj) if type(n[2]) == Person]

    def getNeighborsFromCoords(self, px, py):
        return [n for n in self.getAdjacentsFromCoords(px, py) if type(n[2]) == Person]


    def toString(self):
        s = ""
        for i in range(vsize):
            for j in range(vsize):
                if self.grid[i,j] == -1:
                    s += " "
                elif self.grid[i,j] == None:
                    s += "_"
                else:
                    s += str(self.grid[i,j])
            s += "\n"
        return s

    def getAdults(self):
        return [p for p in self.population if p.isAdult()]

    def getMarrieds(self):
        return [p for p in self.population if p.isMarried()]

    def getSickos(self):
        return [p for p in self.population if p.isSick()]

    def countAdults(self):
        return len(self.getAdults())

    def getBachelors(self):
        return [p for p in self.population if p.isAdult() and not p.isMarried() and p.isMale()]

    def getBachelorettes(self):
        return [p for p in self.population if p.isAdult() and not p.isMarried() and p.isFemale()]
