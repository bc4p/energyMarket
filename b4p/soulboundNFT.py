from . import url, p, config, network, Contract, Accounts
import os 
import json


class SoulBoundNFT():
    def __init__(self):
        from . import Accounts
        self.soulboundNFT = p.SoulBoundToken.deploy({"from": Accounts["faucet"]})

    def __init__(self, deploy=False):
                if(deploy):
                    self.admin = Accounts.new("soul_admin", with_funding=True)
                    self.soulboundNFT = p.SoulBoundToken.deploy({"from": Accounts["faucet"]})
                else:
                    #@TODO: change this to take the abi directly from the build folder
                    with open(os.path.dirname(os.path.realpath(__file__))+'/SoulBound.abi', 'r') as abi_file:
                        eurs_abi_data = json.load(abi_file)
                    self.eurs = Contract.from_abi("SoulBound", config["networks"][network.show_active()]['soulbound']['address'], eurs_abi_data)

    def __str__(self):
        return self.soulboundNFT.__str__()

    def __repr__(self):
        return self.soulboundNFT.__repr__()

    def safeMint(self, account):
        from . import Accounts
        return self.soulboundNFT.safeMint(account.address,account.name, {"from": Accounts["faucet"]})

