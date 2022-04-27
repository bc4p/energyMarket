from collections import Counter
import b4p

class Market():
    def __init__(self):
        self.marketContract = b4p.p.Market
        self.markets = {}

    def new(self, nameMarket, nameAccount, fee=0, connection1=b4p.zero_address, connection2=b4p.zero_address):
        market = self.marketContract.deploy(b4p.EURS,b4p.EnergyToken, connection1, connection2, b4p.Registry, fee, {"from": b4p.Accounts[nameAccount]})
        self.markets[nameMarket] = market


    def setConnections(self, contract, nameAccount, nameMarket1, nameMarket2):
        market = self.markets[contract]
        tx = self.markets[contract].setMarkets(b4p.Market[nameMarket1], b4p.Market[nameMarket2], {"from": b4p.Accounts[nameAccount]})
        tx.wait(1)


    def __getitem__(self, name):
        return self.markets[name]



        


