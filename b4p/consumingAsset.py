from . import p, EursToken, EnergyToken, Accounts
from b4p.utils import print_transaction_events

class ConsumingAssets():
    def __init__(self):
        self.consumingAssetContract = p.ConsumingAsset
        self.consumingAssets = {}

    def new(self,assetName, account, market1):
        from . import Markets, Registry, Accounts, SoulBound
        market = Markets[market1]
        ca = self.consumingAssetContract.deploy(market.address, Registry,SoulBound, {"from": account.address})
        self.consumingAssets[assetName] = ConsumingAsset(ca, account, assetName, market)
        return self.consumingAssets[assetName]

    def __getitem__(self, name):
        if name not in self.consumingAssets:
            raise ValueError(f"asset: {name} not present in available assets:\n{self.consumingAssets}")
        return self.consumingAssets[name]

    def __str__(self):
        return str(self.consumingAssets)

    def __repr__(self):
        return self.consumingAssets


class ConsumingAsset():
    from . import EursToken
    def __init__(self, asset, owner, name, market, with_funding=True):
        self.asset = asset
        self.owner = owner
        self.name = name
        self.market = market
        EursToken.approve(market.address, 10000000*(10**EursToken.decimals()), {"from":owner.address})
        if with_funding:
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

