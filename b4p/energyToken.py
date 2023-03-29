from . import url, p, Contract, config, network, Accounts, EXISTING
import os
import json
class EnergyToken():
        def __init__(self, deploy=EXISTING):
            if(deploy):
                self.admin = Accounts.new("energy_admin", with_funding=True)
                self.energyToken = p.EnergyToken.deploy( "EnergyToken",{"from":Accounts["energy_admin"]})
            else:
                with open(os.path.dirname(os.path.realpath(__file__))+'/EnergyToken.abi', 'r') as abi_file:
                    eurs_abi_data = json.load(abi_file)
                self.energyToken = Contract.from_abi("EnergyToken", config['networks'][network.show_active()]['energy']['address'], eurs_abi_data)


        def __str__(self):
            return self.energyToken.__str__()

        def __repr__(self):
            return self.energyToken.__repr__()

        def balanceOf(self,*args, **kwargs):
            return self.energyToken.balanceOf(*args, **kwargs)

        def totalBalance(self, *args, **kwargs):
            return self.energyToken.totalBalance(*args, **kwargs)

        def transferFrom(self, *args, **kwargs):
            return self.energyToken.transferFrom(*args, **kwargs)