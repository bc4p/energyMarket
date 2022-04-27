import b4p

class ConsumingAsset():
    def __init__(self):
        self.consumingAssetContract = b4p.p.ConsumingAsset
        self.consumingAssets = {}

    def new(self,assetName, accountName, market1):
        market = b4p.Market[market1]
        pa = self.consumingAssetsContract.deploy(market, b4p.Registry, {"from": b4p.Accounts[accountName]})
        self.consumingAssets[assetName] = pa

    def __getitem__(self, name):
        return self.consumingAssets[name]
