from . import p, EursToken,EnergyToken, Accounts
from b4p.utils import print_transaction_events

class ProducingAssets():
    def __init__(self):
        self.producingAssetContract = p.ProducingAsset
        self.produducingAssets = {}

    def new(self,assetName, accountName, market2):
        from . import Markets, Accounts, Registry

        market = Markets[market2]
        account = Accounts[accountName]
        pa = self.producingAssetContract.deploy(market.address, Registry, {"from": account.address})
        self.produducingAssets[assetName] = ProducingAsset(pa, account, assetName, market)
        ##EursToken.transferFrom(Accounts["eurs_admin"].address, self.produducingAssets[assetName].address, 10000)
        ##EnergyToken.transferFrom(Accounts["energy_admin"].address, self.produducingAssets[assetName].address, 10000)
        return self.produducingAssets[assetName]

    def __getitem__(self, name):
        if name in self.produducingAssets:
            return self.produducingAssets[name]
        return False

    def __str__(self):
        return str(self.produducingAssets)

    def __repr__(self):
        return self.produducingAssets




class ProducingAsset():
    def __init__(self, asset, account, name, market, with_funding=True):
        self.asset = asset
        self.owner = account
        self.name = name
        self.market = market
        if with_funding:
            res = EursToken.transfer(self.asset.address, 100*(10**EursToken.decimals()), {"from":Accounts["eurs_admin"]})
            res.wait(1)

    def __repr__(self):
        return self.asset.__repr__()

    def __str__(self):
        return f'<ProducingAsset ({self.name}, {self.owner}, {self.address}, {self.market})>'

    @property
    def address(self):
        return self.asset.__str__()
    
    def createOffer(self, price, amount, id):
        tx = self.asset.createOffer(price*(10**(EursToken.decimals())), amount*(10**6), id, {"from":self.owner})
        tx.wait(1)
        print_transaction_events(tx)



    def acceptBid(self, price, amount, bidId):
        from . import EnergyToken
        final_price = int(price*(10**(EursToken.decimals())))
        final_amount = int(amount*(10**6))
        bidAssetAddress = self.market.bids.getById(bidId).original_market_addresss
        print(bidAssetAddress)

        print("\nBEFORE TRANSACTION\n")
        print(f'    price  {price}EUR | amount {amount}kwh')
        print(f'\n    stablecoin to trasfer {int((final_price)/(10**6))}\n\n    from {bidAssetAddress} | balance {EursToken.balanceOf(bidAssetAddress)}\n    to {self.asset} | balance {self.balanceEURS()}\n')
        print(f'    energytoken to trasfer {amount}\n    from {self.asset} | balance {self.balanceEnergyToken()}\n    to   {bidAssetAddress} | balance {EnergyToken.totalBalance(bidAssetAddress)}\n')

        tx = self.asset.acceptBid(final_price, final_amount, bidId)
        tx.wait(1)

        print("\nAFTER TRANSACTION\n")
        print(f'    from {bidAssetAddress} | balance {EursToken.balanceOf(bidAssetAddress)}\n    to {self.asset} | balance {self.balanceEURS()}\n')
        print(f'    from {self.asset} | balance {self.balanceEnergyToken()}\n    to   {bidAssetAddress} | balance {EnergyToken.totalBalance(bidAssetAddress)}\n')
        print_transaction_events(tx)

    def balanceEURS(self):
        return EursToken.balanceOf(self.asset)

    def balanceEnergyToken(self):
        from . import EnergyToken
        return EnergyToken.totalBalance(self.asset)
    
    



