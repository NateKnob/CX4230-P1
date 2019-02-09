import random
from collections import Counter
from entities.humans import Person, Farmer

commodities = ["food", "stress"]

class Village:
    def __init__(self, size=random.randint(10, 20)):
        self.population = [Farmer() for i in range(size)]
        self.wealth = Counter({"food": 200})
        self.metrics = Counter()

    def getAge(self):
        return self.age

    def work(self):
        self.metrics = Counter()

        harvest = Counter()
        consumed = Counter()

        for i, citizen in enumerate(reversed(self.population)):
            consumption = citizen.eat(self)
            for key in consumption:
                if key in commodities:
                    if self.wealth[key] + consumption[key] >= 0:
                        self.wealth[key] += consumption[key]
                    else:
                        citizen.die()
                        self.metrics["deaths"] += 1
                else:
                    self.metrics[key] += consumption[key]
        self.population = [citizen for citizen in self.population if not citizen.isDead()]

        for i, citizen in enumerate(self.population):
            product = citizen.work(self)
            for key in product:
                harvest[key] += product[key]
            if "death" in product:
                citizen.die()
                self.metrics["deaths"] += 1
        self.population = [citizen for citizen in self.population if not citizen.isDead()]

        for key in harvest:
            if key in commodities:
                self.wealth[key] += harvest[key]

        if harvest["birth"] > 0:
            for b in range(harvest["birth"]):
                self.population.append(Farmer())
                self.metrics["births"] += 1

        print("Marrieds :", len(self.getMarrieds()))
        print("Sick     :", len(self.getSickos()))
        print("Births   :", self.metrics["births"])
        print("Starved  :", self.metrics["deaths"])
        print("Food     :", self.wealth["food"])

        bm = self.getBachelors()
        bf = self.getBachelorettes()
        for i in range(min(len(bm), len(bf))):
            bm[i].marry(bf[i])
            bf[i].marry(bm[i])

        return harvest

    def getPopStats(self):
        olds = 0
        youths = 0
        adults = 0
        sickos = 0
        total = 0
        for p in self.population:
            total += 1
            adults += p.isAdult()
            youths += p.isYoung()
            olds += p.isOld()
            sickos += p.isSick()
        return [olds, youths, adults, sickos, total,
            self.wealth["food"], self.metrics["births"], self.metrics["deaths"], self.metrics["illDeaths"]]

    def toString(self):
        s = ""
        for citizen in self.population:
            s += citizen.toString()
        return s

    def getAdults(self):
        return [p for p in self.population if p.isAdult() ]

    def getMarrieds(self):
        return [p for p in self.population if p.isMarried() ]

    def getSickos(self):
        return [p for p in self.population if p.isSick()]

    def countAdults(self):
        return len(self.getAdults())

    def getBachelors(self):
        return [p for p in self.population if p.isAdult() and not p.isMarried() and p.isMale() ]

    def getBachelorettes(self):
        return [p for p in self.population if p.isAdult() and not p.isMarried() and p.isFemale() ]
