
import b4p
class Registry():

    def __init__(self):
        self.registry = b4p.p.MarketRegistry.deploy({"from": b4p.Accounts["admin"]})
        print(self.registry)


    def __str__(self):
        return self.registry.__str__()

    def __repr__(self):
        return self.registry.__repr__()

