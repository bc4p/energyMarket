from . import p, EursToken, EnergyToken, Accounts
import b4p
from b4p.utils import print_transaction_events

class ConsumingAssets():
    def __init__(self):
        self.consumingAssetContract = p.ConsumingAsset
        self.consumingAssets = {}

    def new(self,assetName, accountName, market1):
        from . import Markets, Registry, Accounts
        market = Markets[market1]
        account = Accounts[accountName]
        ca = self.consumingAssetContract.deploy(market.address, Registry, {"from": account.address})
        self.consumingAssets[assetName] = ConsumingAsset(ca, account, assetName, market)
        return self.consumingAssets[assetName]

    def __getitem__(self, name):
        if name in self.consumingAssets:
            return self.consumingAssets[name]
        return False

    def __str__(self):
        return str(self.consumingAssets)

    def __repr__(self):
        return self.consumingAssets


class ConsumingAsset():
    def __init__(self, asset, owner, name, market):
        self.asset = asset
        self.owner = owner
        self.name = name
        self.market = market
        res = EursToken.transfer(self.asset.address, 5000*(10**EursToken.decimals()), {"from":Accounts["eurs_admin"]})
        res.wait(1)

    def __repr__(self):
        return self.asset.__repr__()

    def __str__(self):
        return f'<ConsumingAsset ({self.name}, {self.owner}, {self.asset}, {self.market})>'

    @property
    def address(self):
        return self.asset.__str__()
        
    def createBid(self, price, amount, id):
        tx = self.asset.createBid(price*(10**(EursToken.decimals())), amount*(10**6), id, {"from":self.owner})
        tx.wait(1)
        print_transaction_events(tx)
    
    def balanceEURS(self):
        return EursToken.balanceOf(self.asset)

    def balanceEnergyToken(self):
        from . import EnergyToken
        return EnergyToken.balanceOf(self.asset)

