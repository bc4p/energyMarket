from collections import Counter
from . import p, zero_address, EursToken, Accounts
import logging

class Markets():

    def __init__(self):
        self.marketContract = p.Market
        self.markets = {}

    def new(self, nameMarket, nameAccount, fee=0, connection1= zero_address, connection2=zero_address):
        from . import EnergyToken, Registry, Accounts
        #TODO: check if account exists before deploying the market
        account =  Accounts[nameAccount]
        market = self.marketContract.deploy( EursToken, EnergyToken, connection1, connection2,  Registry, fee, {"from": account.address})
        self.markets[nameMarket] = Market(market, account, nameMarket)
        return self.markets[nameMarket]
    
    def __str__(self):
        return str(self.markets)

    def __getitem__(self, name):
        if name in self.markets:
            return self.markets[name]
        return False

class Market():
    def __init__(self, market, account, name):
        self.market = market
        EursToken.transfer(self.market.address, 50 * 10**(EursToken.decimals()), {"from":  Accounts["eurs_admin"]})
        self.owner = account
        self.name = name

    class Offers():
        class Offer():
            def __init__(self, offer):
                self.created_at = offer[0]
                self.price = offer[1]
                self.amount = offer[2]
                self.original_market_addresss = offer[3]
                self.last_market_address = offer[4]
                self.id = offer[6]
            
            def __repr__(self):
                return f'<Offer({self.created_at}, {self.price}, {self.amount}, {self.original_market_addresss}, {self.last_market_address})>'
                
        def __init__(self, market):
            self.market = market

        def __len__(self):
            return self.market.offersLength()

        def __getitem__(self, index):
            if len(self) < index:
                raise IndexError(f'offer with index {index} out of range for offers of length {len(self)}')
            return self.Offer(self.market.offers(index))

        def __repr__(self):
            string = "["
            for i in range(0, len(self)):
                string+=str(self[i])+'\n'
            return string+"]"

        def getById(self, offerId):
            for i in range(0, len(self)):
                if self[i].id == offerId:
                    return self[i]


        def indexOf(self, offer):
            for i in self:
                temp_offer = self[i]
                if temp_offer.id == offer.id:
                    return i
            return False

        


        
    class Bids():
        class Bid():
            def __init__(self, bid):
                self.created_at = bid[0]
                self.price = bid[1]
                self.amount = bid[2]
                self.original_market_addresss = bid[3]
                self.last_market_address = bid[4]
                self.id = bid[6]
            
            def __repr__(self):
                return f'<Bid({self.created_at}, {self.price}, {self.amount}, {self.original_market_addresss}, {self.last_market_address})>'
            
        def __init__(self, market):
            self.market = market

        def __len__(self):
            return self.market.bidsLength()

        def __getitem__(self, index):
            if len(self) < index:
                raise IndexError(f'index {index} out of range for bids of length {len(self)}')
            return self.Bid(self.market.bids(index))

        def __repr__(self):
            string = "["
            for i in range(0, len(self)):
                string+=str(self[i])+'\n'
            return string+"]"

        def getById(self, bidId):
            for i in range(0, len(self)):
                if self[i].id == bidId:
                    return self[i]

        def indexOf(self, bid):
            for i in self:
                temp_bid = self[i]
                if temp_bid.id == bid.id:
                    return i
            return False


    @property
    def offers(self):
        return self.Offers(self.market)

    @property
    def bids(self):
        return self.Bids(self.market)

    @property
    def address(self):
        return self.market.__str__()
              
    def __str__(self):
        return f'<Market ({self.name}, {self.address})>'

    def __repr__(self):
        return self.market.__repr__()

    def setConnections(self, nameMarket1=zero_address, nameMarket2=zero_address):
        import b4p

        tx = self.market.setMarkets(b4p.Markets[nameMarket1], b4p.Markets[nameMarket2], {"from": self.owner})
        tx.wait(1)

    def forwardOffer(self, id):
        tx = self.market.forwardOffer(id, {"from": self.owner})
        tx.wait(1)

    def forwardBid(self, id):
        tx = self.market.forwardBid(id, {"from": self.owner})
        tx.wait(1)

    def balanceEURS(self):
        return  EursToken.balanceOf(self.market)

    def balanceEnergyToken(self):
        from . import EnergyToken
        return EnergyToken.balanceOf(self.market)

    def status(self):
        print(f'\n\n°°°°°°°°°° MARKET STATUS °°°°°°°°°°\nNUM OFFERS: {self.offers}  |  NUM BIDS: {self.bids}\n\n')

    def fee(self):
        return self.market.fee()

    def set_fee(self,new_fee):
        self.market.setFee(new_fee)

    

