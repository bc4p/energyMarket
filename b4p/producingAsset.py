from . import p, EURS, FAUCET
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
    def __init__(self, asset, account, name, market):
        self.asset = asset
        self.owner = account
        self.name = name
        self.market = market
        EURS.transfer(self.asset, 1000*(10**EURS.decimals()), {"from":FAUCET})

    def __repr__(self):
        return self.asset.__repr__()

    def __str__(self):
        return f'<ProducingAsset ({self.name}, {self.owner}, {self.address}, {self.market})>'

    @property
    def address(self):
        return self.asset.__str__()
    
    def createOffer(self, price, amount, id):
        tx = self.asset.createOffer(price*(10**(EURS.decimals())), amount*(10**6), id, {"from":self.owner})
        tx.wait(1)
        print_transaction_events(tx)



    def acceptBid(self, price, amount, bidId):
        from . import EnergyToken
        final_price = int(price*(10**(EURS.decimals())))
        final_amount = int(amount*(10**6))
        bidAssetAddress = self.market.bids.getById(bidId).original_market_addresss

        print("\nBEFORE TRANSACTION\n")
        print(f'    price  {price}EUR | amount {amount}kwh | tot {price*amount}')
        print(f'\n    stablecoin to trasfer {int((final_price*final_amount)/(10**6))}\n\n    from {bidAssetAddress} | balance {EURS.balanceOf(bidAssetAddress)}\n    to {self.asset} | balance {self.balanceEURS()}\n')
        print(f'    energytoken to trasfer {amount}\n    from {self.asset} | balance {self.balanceEnergyToken()}\n    to   {bidAssetAddress} | balance {EnergyToken.balanceOf(bidAssetAddress)}\n')

        tx = self.asset.acceptBid(final_price, final_amount, bidId)
        tx.wait(1)

        print("\nAFTER TRANSACTION\n")
        print(f'    from {bidAssetAddress} | balance {EURS.balanceOf(bidAssetAddress)}\n    to {self.asset} | balance {self.balanceEURS()}\n')
        print(f'    from {self.asset} | balance {self.balanceEnergyToken()}\n    to   {bidAssetAddress} | balance {EnergyToken.balanceOf(bidAssetAddress)}\n')
        print_transaction_events(tx)

    def balanceEURS(self):
        return EURS.balanceOf(self.asset)

    def balanceEnergyToken(self):
        from . import EnergyToken
        return EnergyToken.balanceOf(self.asset)
    
    



