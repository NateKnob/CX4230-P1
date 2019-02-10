import random

from entities.occupation import *

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
    def __init__(self, age=0, occupation=Unemployed()):
        self.age = age
        self.lifespan = random.randint(14, 18)
        self.partner = None
        self.occupation = occupation
        self.sex = random.randint(0, 1)
        self.alive = True
        self.sick = 0

    def work(self, village):
        if self.isAdult():
            occupation = Farmer() if random.randint(0, 5) < village.foodNeed else Worker()
        else:
            occupation = Unemployed()
        self.occupation = occupation
        self.occupation.work(village)

    def disease(self, village):
        if random.random() < sickChance:
            self.fallIll()

        if self.isSick():
            if random.random() < illKillChance:
                self.die()
                village.metrics["illDeaths"] += 1
            else:
                self.sick += 1
                if self.sick > sickRecovery:
                    self.sick = -1

        crowding = len(village.population) / village.area
        if random.random() < infectionChance * crowding:
            self.infect(village.population[random.randint(0, len(village.population) - 1)])

    def procreate(self):
        if self.isMarried() and not self.isOld() \
                and self.isFemale() and random.random() < birthChance:
            return True

        self.age += 1
        if self.age > self.lifespan:
            self.die()

    def getAge(self):
        return self.age
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
    def isAlive(self):
        return self.alive
    def die(self):
        self.alive = False
    def isSick(self):
        return self.sick > 0
    def fallIll(self):
        if self.sick == 0:
            self.sick = 1
    def infect(self, friend):
        friend.fallIll()

    def toString(self):
        if self.age <= youth:
            return "v"
        elif self.age >= elder:
            return ")"
        elif self.isMarried():
            return "%"
        return "|"


class PersonFactory:
    def __init__(self):
        pass

    @staticmethod
    def makeRandomWorker():
        age = random.randint(3, 12)
        occupation = Farmer() if random.randint(0, 1) > 0 else Worker()
        return Person(age, occupation)

    @staticmethod
    def makeRandomPerson():
        age = random.randint(0, 18)
        if age > youth and age < elder:
            occupation = Farmer() if random.randint(0, 2) > 0 else Worker()
        else:
            occupation = Unemployed()
        return Person(age, occupation)
