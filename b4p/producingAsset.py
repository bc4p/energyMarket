import b4p

class ProducingAssets():
    def __init__(self):
        self.producingAssetContract = b4p.p.ProducingAsset
        self.produducingAssets = {}

    def new(self,assetName, accountName, market2):
        market = b4p.Markets[market2]
        account = b4p.Accounts[accountName]
        pa = self.producingAssetContract.deploy(market, b4p.Registry, {"from": account})
        self.produducingAssets[assetName] = ProducingAsset(pa, account)
        return self.produducingAssets[assetName]

    def __getitem__(self, name):
        return self.produducingAssets[name]




class ProducingAsset():
    def __init__(self, asset, account):
        self.asset = asset
        self.owner = account

    def __str__(self):
        return self.asset.__str__()

    def __repr__(self):
        return self.asset.__repr__()

    def createOffer(self, price, amount):
        tx = self.asset.createOffer(price, amount, {"from": self.owner})
        tx.wait(1)
    
    def balanceEURS(self):
        return b4p.EURS.balanceOf(self.asset)

    def balanceEnergyToken(self):
        return b4p.EnergyToken.balanceOf(self.asset)



