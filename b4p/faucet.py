
from . import url, p, Contract, config, network, EXISTING
from brownie.network import accounts

class Faucet():

    def __init__(self, existing=EXISTING):
        if(existing):
            print(network)
            self.faucet = accounts.at(config["networks"][network.show_active()]['eurs']['faucet'], force=True)
            print(self.faucet.address)
            
    def __str__(self):
        return self.faucet.__str__()

    def __repr__(self):
        return self.faucet.__repr__()