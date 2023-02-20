from . import url, p, config, network, Contract, Accounts
import os 
import json
class EursToken():
        def __init__(self, deploy=False):
            if(deploy):
                self.admin = Accounts.new("eurs_admin", with_funding=True)
                self.eurs = p.EursMock.deploy({"from":Accounts["eurs_admin"]})
                #self.eurs.createTokens(1000000*(10**self.eurs.decimals()),{"from":Accounts["eurs_admin"]})
                print("EURS deployed")
            else:
                with open(os.path.dirname(os.path.realpath(__file__))+'/ERC20.abi', 'r') as abi_file:
                    eurs_abi_data = json.load(abi_file)
                self.eurs = Contract.from_abi("EursMock", config["networks"][network.show_active()]['eurs']['address'], eurs_abi_data)

        def __str__(self):
            return self.eurs.__str__()

        def __repr__(self):
            return self.eurs.__repr__()
        
        def transfer(self, *args, **kwargs):
            return self.eurs.transfer(*args, **kwargs)

        def balanceOf(self, *args, **kwargs):
            return self.eurs.balanceOf(*args, **kwargs)

        def decimals(self, *args, **kwargs):
                return self.eurs.decimals(*args, **kwargs)

        def transferFrom(self, *args, **kwargs):
            return self.eurs.transferFrom(*args, **kwargs)