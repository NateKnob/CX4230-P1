from abc import abstractmethod
import random


class Occupation:
    def __init__(self):
        pass

    @abstractmethod
    def work(self, village):
        raise NotImplementedError()


class Unemployed(Occupation):
    def __init__(self):
        super().__init__()

    def work(self, village):
        pass


class Farmer(Occupation):
    def __init__(self):
        super().__init__()

    def work(self, village):
        village.wealth['food'] += random.randint(80, 120)


class Worker(Occupation):
    def __init__(self):
        super().__init__()

    def work(self, village):
        village.wealth['wood'] += random.randint(80, 120)


class Soldier(Occupation):
    def __init__(self):
        super().__init__()

    def work(self, village):
        pass

    def fight(self, village):
        pass
