from collections import Counter
import b4p

class Markets():
    def __init__(self):
        self.marketContract = b4p.p.Market
        self.markets = {}
        self.markets[b4p.zero_address] = b4p.zero_address

    def new(self, nameMarket, nameAccount, fee=0, connection1=b4p.zero_address, connection2=b4p.zero_address):
        account = b4p.Accounts[nameAccount]
        market = self.marketContract.deploy(b4p.EURS,b4p.EnergyToken, connection1, connection2, b4p.Registry, fee, {"from": account})
        self.markets[nameMarket] = Market(market, account)
        return self.markets[nameMarket]

    def __getitem__(self, name):
        return self.markets[name]

class Market():
    def __init__(self, market, account):
        self.market = market
        b4p.EURS.transfer(self.market, 1000, {"from": b4p.EURS})
        self.owner = account

    def __str__(self):
        return self.market.__str__()

    def __repr__(self):
        return self.market.__repr__()

    def setConnections(self, nameMarket1=b4p.zero_address, nameMarket2=b4p.zero_address):
        tx = self.market.setMarkets(b4p.Markets[nameMarket1], b4p.Markets[nameMarket2], {"from": self.owner})
        tx.wait(1)

    def forwardOffer(self, id):
        tx = self.market.forwardOffer(id, {"from": self.owner})
        tx.wait(1)

    def forwardBid(self, id):
        tx = self.market.forwardBid(id, {"from": self.owner})
        tx.wait(1)
        print(tx.call_trace())

    def balanceEURS(self):
        return b4p.EURS.balanceOf(self.market)

    def balanceEnergyToken(self):
        return b4p.EnergyToken.balanceOf(self.market)

    


        


