from . import EURS, FAUCET
from brownie.network import accounts

class Accounts():
    def __init__(self):
        self.accounts = {}
        self.accounts["admin"] = Account(accounts.add(), "admin")
        EURS.transfer(self.accounts["admin"].address, 1000, {"from":  FAUCET})
        

    def __getitem__(self, name):
        if name in self.accounts:
            return self.accounts[name]
        return False

    def __str__(self):
        return str(self.accounts)

    def __repr__(self):
        return self.accounts

    def new(self, name):
        self.accounts[name] = Account(accounts.add(),name)
        EURS.transfer(self.accounts[name].address, 1000, {"from":  FAUCET})
        return self.accounts[name]

class Account():

    def __init__(self, account,name):
        self.account = account
        self.name = name
        
    @property
    def address(self):
        return self.account.__str__()
        
    def __repr__(self):
        return self.account.__repr__()

    def __str__(self):
        return f'<Account ({self.name}, {self.address})>'

    def deploy(self, *args, **kwargs):
        return self.account.deploy(*args, **kwargs)

    def transfer(self, *args, **kwargs):
        return self.account.transfer(*args, **kwargs)

    def balanceEURS(self):
        return EURS.balanceOf(self.account)

    def balanceEnergyToken(self):
        from . import EnergyToken
        return EnergyToken.balanceOf(self.account)






    