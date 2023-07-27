from . import p
class SoulBound():
    def __init__(self):
        from . import Accounts
        
        self.soulbound = p.SoulBoundToken.deploy({"from": Accounts["faucet"]})


    def __str__(self):
        return self.soulbound.__str__()

    def __repr__(self):
        return self.soulbound.__repr__()
    
    def balanceOf(self,*args, **kwargs):
        return self.soulbound.balanceOf(*args, **kwargs)

    def createIdentity(self, account, info):
        soulbound = self.soulbound.safeMint(account.address,info)
        return soulbound
    
    def assets(self, address):
        num_address = self.soulbound.numAssets(address)
        assets = []
        for i in range(num_address):
            assets.append(self.soulbound.assets(address, i))
        return assets

