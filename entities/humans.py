import random

youth = 3
elder = 10
birthChance = 0.25

class Person:
    def __init__(self, age=0):
        self.age = age
        self.lifespan = random.randint(14, 18)
        self.partner = None

    def getAge(self):
        return self.age

    def work(self, village):
        self.age += 1
        product = { "stress": 1 }
        if self.age > self.lifespan:
            product["death"] = 1
        if self.isMarried() and not self.isOld() and random.random() < birthChance:
            product["birth"] = 1

        return product

    def toString(self):
        if self.age <= youth:
            return "v"
        elif self.age >= elder:
            return ")"
        elif self.isMarried():
            return "%"

        return "|"

    def isAdult(self):
        return self.age > youth

    def isOld(self):
        return self.age >= elder

    def isMarried(self):
        return self.partner != None

    def marry(self, partner):
        self.partner = partner

class Farmer(Person):
    def __init__(self, age=0):
        super().__init__(0)

    def work(self, village):
        product = super().work(village)
        product["food"] = 1
        return product
