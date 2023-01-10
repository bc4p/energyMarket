from . import p
class Registry():

    def __init__(self):
        from . import Accounts
        self.registry = p.MarketRegistry.deploy({"from": Accounts["faucet"]})


    def __str__(self):
        return self.registry.__str__()

    def __repr__(self):
        return self.registry.__repr__()

    def getMarkets(self):
        markets = self.registry.getMarkets()
        return markets

