import random
from collections import Counter
from entities.humans import Person, Farmer

class Village:
    def __init__(self, size=random.randint(5, 10)):
        self.population = [Farmer() for i in range(size)]

    def getAge(self):
        return self.age

    def work(self):
        harvest = Counter()
        for i, citizen in enumerate(self.population):
            product = citizen.work(self)
            for key in product:
                harvest[key] += product[key]
            if "death" in product:
                del self.population[i]

        print("Marrieds :", len(self.getMarrieds()))

        print("Births   :", harvest["birth"])
        if harvest["birth"] > 0:
            for b in range(harvest["birth"]):
                self.population.append(Farmer())

        bachelors = self.getBachelors()
        while len(bachelors) > 4:
            bachelors[-1].marry(bachelors[-2])
            bachelors[-2].marry(bachelors[-1])
            bachelors = self.getBachelors()

        return harvest


    def toString(self):
        s = ""
        for citizen in self.population:
            s += citizen.toString()
        return s

    def getAdults(self):
        return [p for p in self.population if p.isAdult() ]

    def getMarrieds(self):
        return [p for p in self.population if p.isMarried() ]

    def countAdults(self):
        return len(self.getAdults())

    def getBachelors(self):
        return [p for p in self.population if p.isAdult() and not p.isMarried() ]
