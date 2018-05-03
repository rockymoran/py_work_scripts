class Car():
    def __init__(self, modelname, yearm, price):
        self.modelname = modelname
        self.yearm = yearm
        self.price = price

    def price_increase(self):
        self.price = int(self.price * 1.15)


class SuperCar(Car):
    def __init__(self, modelname, yearm, price, cc):
        super.__init__(modelname, yearm, price)
        self.cc = cc

honda = SuperCar('City', 2017, 100000)
tata = Car('Zap', 2016, 600000)

honda.cc = 1500
tata.cc = 2500

# print(help(honda))
# print(honda.yearm)
