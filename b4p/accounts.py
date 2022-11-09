from . import EURS
from brownie.network import accounts


class Accounts():
    def __init__(self,accountname="",with_name=False):
        self.accounts = {}
        if with_name==False:
            self.accounts["admin"] = Account(accounts.add())
        else:
            self.accounts["admin"] = Account(accounts.at(accountname, force=True))
        #cannot do this in FH blockchain
        #EURS.transfer(self.accounts["admin"], amount, {"from":  EURS})
        pass

    def __getitem__(self, name):
        if name in self.accounts:
            return self.accounts[name]
        return False


    def new(self, name):
        self.accounts[name] = Account(accounts.add())
        #EURS.transfer(self.accounts[name], 1000, {"from":  EURS})
        return self.accounts[name]

class Account():

    def __init__(self, account):
        self.account = account

    def __str__(self):
        return self.account.__str__()

    def __repr__(self):
        return self.account.__repr__()

    def deploy(self, *args, **kwargs):
        return self.account.deploy(*args, **kwargs)

    def transfer(self, *args, **kwargs):
        return self.account.transfer(*args, **kwargs)

    def balanceEURS(self):
        return EURS.balanceOf(self.account)

    def balanceEnergyToken(self):
        from . import EnergyToken
        return EnergyToken.balanceOf(self.account)






    