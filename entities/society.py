import random
from collections import Counter
from entities.humans import *
from entities.occupation import *

min_food = 12
good_food = 20


class Village:
    def __init__(self, size=random.randint(10, 20)):
        self.population = [PersonFactory.makeRandomPerson() for _ in range(size)]
        self.area = size * 2
        self.foodNeed = 3
        self.wealth = Counter({"food": size * 100, "wood": size * 100, "gold": 0})
        self.metrics = Counter()
        self.happiness = 70

    def _clean(self, reason):
        before = len(self.population)
        self.population = [person for person in self.population if person.isAlive()]
        self.metrics["deaths_" + reason] += (before - len(self.population))

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
        for _ in range(births):
            self.population.append(Person())

    def _build(self):
        if len(self.population) > self.area:
            self.area += self.wealth['wood'] // 100
            self.wealth['wood'] %= 100
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
        return [len(self.population), self.countAdults(), len([p for p in self.population if type(p.occupation) == Farmer]),
                len([p for p in self.population if type(p.occupation) == Worker]), len(self.getMarrieds()),
                self.wealth["food"], self.wealth["wood"], self.wealth["gold"], self.metrics["deaths_starve"],
                len(self.getSickos()), self.metrics["deaths_plague"], self.happiness]

    def toString(self):
        s = ""
        for citizen in self.population:
            s += citizen.toString()
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
