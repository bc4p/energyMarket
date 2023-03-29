from . import url, p, config, network, Contract, Accounts
import os 
import json

class SoulBoundNFT():

    def __init__(self, deploy=True):
        if(deploy):
            self.admin = Accounts.new("soul_admin", with_funding=True)
            self.soulboundNFT = p.SoulBoundToken.deploy({"from": Accounts["faucet"]})
        else:
            #@TODO: change this to take the abi directly from the build folder
            with open(os.path.dirname(os.path.realpath(__file__))+'/SoulBound.abi', 'r') as abi_file:
                eurs_abi_data = json.load(abi_file)
            self.soulboundNFT = Contract.from_abi("SoulBound", config["networks"][network.show_active()]['soulbound']['address'], eurs_abi_data)

    def __str__(self):
        return self.soulboundNFT.__str__()

    def __repr__(self):
        return self.soulboundNFT.__repr__()

    def safeMint(self, account, data):
        from . import Accounts
        return self.soulboundNFT.safeMint(account.address, json.dumps(data), {"from": Accounts["faucet"]})


    def add_asset_data(self, cons_asset, data):
        from . import Accounts
        print(cons_asset)
        account_id = cons_asset.account_id
        print(account_id)
        account = Accounts[account_id]
        current_data = self.soulboundNFT.image(account.address)
        json_data = json.loads(current_data)

        json_data[cons_asset.address] = data
        token_id = self.soulboundNFT.tokenOfOwnerByIndex(account.address, 0)

        self.soulboundNFT.updateMetadata(token_id, json.dumps(json_data), {"from": account})
     
        print(json_data)
        return current_data

    def get_data(self, account_id):
        from . import Accounts
        account = Accounts[account_id]
        current_data = self.soulboundNFT.image(account.address)
        json_data = json.loads(current_data)
        return json_data

    def get_asset_data(self, cons_asset):
            json_data = self.get_data(cons_asset.account_id)
            return json_data[cons_asset.address]


    def compute_utility(self, const_asset, offer):
        data = self.get_asset_data(const_asset)
        return 0

    def highiest_utility_offer(self, asset, market):
        highiest_index = -1
        highiest_utitlity = 0
        for offer, i in enumerate(market.offers):
            u = self.compute_utility(asset, offer)
            print(u)
            if u > highiest_utitlity:
                highiest_index = u
        if highiest_index != -1:
            return market.offers[highiest_index]
        else:
            return False
        

            

