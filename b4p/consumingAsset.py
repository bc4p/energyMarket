import b4p

class ConsumingAssets():
    def __init__(self):
        self.consumingAssetContract = b4p.p.ConsumingAsset
        self.consumingAssets = {}

    def new(self,assetName, accountName, market1):
        market = b4p.Markets[market1]
        account = b4p.Accounts[accountName]
        ca = self.consumingAssetContract.deploy(market, b4p.Registry, {"from": account})
        self.consumingAssets[assetName] = ConsumingAsset(ca,account)
        return self.consumingAssets[assetName]

    def __getitem__(self, name):
        return self.consumingAssets[name]



class ConsumingAsset():
    def __init__(self, asset, owner):
        self.asset = asset
        b4p.EURS.transfer(self.asset, 1000, {"from": b4p.EURS})
        self.owner = owner

    def __str__(self):
        return self.asset.__str__()

    def __repr__(self):
        return self.asset.__repr__()
        
    def createBid(self, price, amount):
        tx = self.asset.createBid(price, amount, {"from":self.owner})
        tx.wait(1)
    
    def balanceEURS(self):
        return b4p.EURS.balanceOf(self.asset)

    def balanceEnergyToken(self):
        return b4p.EnergyToken.balanceOf(self.asset)

