import b4p

class ProducingAsset():
    def __init__(self):
        self.producingAssetContract = b4p.p.ProducingAsset
        self.produducingAssets = {}

    def new(self,assetName, accountName, market2):
        market = b4p.Market[market2]
        pa = self.producingAssetContract.deploy(market, b4p.Registry, {"from": b4p.Accounts[accountName]})
        self.produducingAssets[assetName] = pa

    def __getitem__(self, name):
        return self.produducingAssets[name]
