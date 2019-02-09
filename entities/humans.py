import random

youth = 3
elder = 12
birthChance = 0.5

sickChance = 0.02
infectionChance = 0.8
illKillChance = 0.2
sickRecovery = 3

# sex:
# 0 = female
# 1 = male

class Person:
    def __init__(self, age=0):
        self.age = age
        self.lifespan = random.randint(14, 18)
        self.partner = None
        self.hunger = 1
        self.sex = random.randint(0, 1)
        self.dead = False
        self.sick = 0

    def getAge(self):
        return self.age

    def getHunger(self):
        return self.hunger

    def eat(self, vilage):
        consumption = { "food": -self.hunger }

        if self.isSick():
            if random.random() < illKillChance:
                self.die()
                consumption["illDeaths"] = 1
            else:
                self.sick += 1
                if self.sick > sickRecovery:
                    self.sick = -1
        if random.random() < sickChance:
            self.fallIll()

        return consumption

    def work(self, village):
        self.age += 1
        product = { "stress": 1 }
        if self.age > self.lifespan:
            self.die()
        if self.isMarried() and not self.isOld() and self.isMarried() and self.isFemale() and random.random() < birthChance:
            product["birth"] = 1

        return product

    def toString(self):
        if self.age <= youth:
            return "v"
        elif self.age >= elder:
            return ")"
        elif self.isMarried():
            return "%"
        # if self.isSick():
        #     return str(self.sick)
        # if self.sick == -1:
        #     return "T"

        return "|"

    def isYoung(self):
        return self.age <= youth

    def isAdult(self):
        return self.age > youth

    def isOld(self):
        return self.age >= elder

    def isMarried(self):
        return self.partner != None

    def marry(self, partner):
        self.partner = partner

    def isMale(self):
        return self.sex == 1

    def isFemale(self):
        return self.sex == 0

    def isDead(self):
        return self.dead

    def die(self):
        self.dead = True

    def isSick(self):
        return self.sick > 0

    def fallIll(self):
        if (self.sick == 0):
            self.sick = 1

    def infect(self, friend):
        if random.random() < infectionChance:
            friend.fallIll()

class Farmer(Person):
    def __init__(self, age=0):
        super().__init__(age)

    def work(self, village):
        product = super().work(village)
        if (self.isAdult() and not self.isOld()):
            product["food"] = 2
        return product
