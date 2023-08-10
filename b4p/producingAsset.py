from . import p, EursToken,EnergyToken, Accounts
from b4p.utils import print_transaction_events
import time
class ProducingAssets():
    def __init__(self):
        self.producingAssetContract = p.ProducingAsset
        self.produducingAssets = {}

    def new(self,assetName, account, market2):
        from . import Markets, Accounts, Registry, SoulBound

        market = Markets[market2]
        pa = self.producingAssetContract.deploy(market.address, Registry,SoulBound,{"from": account.address})
        self.produducingAssets[assetName] = ProducingAsset(pa, account, assetName, market)
        ##EursToken.transferFrom(Accounts["eurs_admin"].address, self.produducingAssets[assetName].address, 10000)
        ##EnergyToken.transferFrom(Accounts["energy_admin"].address, self.produducingAssets[assetName].address, 10000)
        return self.produducingAssets[assetName]

    def __getitem__(self, name):
        if name not in self.produducingAssets:
            raise ValueError(f"asset: {name} not present in available assets:\n{self.produducingAssets}")
        return self.produducingAssets[name]


    def __str__(self):
        return str(self.produducingAssets)

    def __repr__(self):
        return self.produducingAssets




class ProducingAsset():
    from . import EursToken
    def __init__(self, asset, account, name, market, with_funding=True):
        self.asset = asset
        self.owner = account
        self.name = name
        self.market = market
        EursToken.approve(market.address, 100000, {"from":account.address})
        if with_funding:
            res = EursToken.transfer(self.asset.address, 5000*(10**EursToken.decimals()), {"from":Accounts["eurs_admin"]})
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



    def acceptBid(self, price, amount, bidId, seller_id, buyer_id):
        from . import EnergyToken, EursToken
        import b4p
        final_price = int(price*(10**(EursToken.decimals())))
        final_amount = int(amount*(10**6))
        bid = self.market.bids.getById(bidId)
        bidAssetAddress = bid.original_market_addresss
        onwerAddress = self.owner.address

        eursBalanceBidder = EursToken.balanceOf(bidAssetAddress)
        balanceOwner = EursToken.balanceOf(onwerAddress)
        balanceEnergyOwner = EnergyToken.totalBalance(onwerAddress)
        balanceEnergyReceiver = EnergyToken.totalBalance(bidAssetAddress)

        b4p.logger.log_dictionary({"EUR":eursBalanceBidder, "ENERGY":balanceEnergyReceiver, "timestamp":time.time()}, f"{buyer_id}_BALANCE")
        b4p.logger.log_dictionary({"EUR":balanceOwner, "ENERGY":balanceEnergyOwner, "timestamp":time.time()}, f"{seller_id}_BALANCE")
        print(bidAssetAddress)

        print("\nBEFORE TRANSACTION\n")
        print(f'    price  {price}EUR | amount {amount}kwh')
        print(f'\n    stablecoin to trasfer {int((final_price)/(10**6))}\n\n    from {bidAssetAddress} | balance {eursBalanceBidder}\n    to {onwerAddress} | balance {balanceOwner}\n')
        print(f'    energytoken to trasfer {amount}\n    from {onwerAddress} | balance {balanceEnergyOwner}\n    to   {bidAssetAddress} | balance {balanceEnergyReceiver}\n')

        tx = self.asset.acceptBid(final_price, final_amount, bidId)
        tx.wait(1)
        eursBalanceBidder = EursToken.balanceOf(bidAssetAddress)
        balanceOwner = EursToken.balanceOf(onwerAddress)
        balanceEnergyOwner = EnergyToken.totalBalance(onwerAddress)
        balanceEnergyReceiver = EnergyToken.totalBalance(bidAssetAddress)

        print("\nAFTER TRANSACTION\n")
        print(f'    from {bidAssetAddress} | balance {eursBalanceBidder}\n    to {onwerAddress} | balance {balanceOwner}\n')
        print(f'    from {onwerAddress} | balance {balanceEnergyOwner}\n    to   {bidAssetAddress} | balance {balanceEnergyReceiver}\n')
        print_transaction_events(tx)


    def balanceEURS(self):
        return EursToken.balanceOf(self.asset)

    def balanceEnergyToken(self):
        from . import EnergyToken
        return EnergyToken.totalBalance(self.asset)
    
    



