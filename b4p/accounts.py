import b4p
from brownie.network import accounts


class Accounts():
    def __init__(self):
        self.accounts = {}
        self.accounts["admin"] = Account(accounts[0])
        self.counter = 1
        pass

    def __getitem__(self, name):
        return self.accounts[name]


    def new(self, name):
        self.accounts[name] = Account(accounts[self.counter])
        self.counter += 1
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
        return b4p.EURS.balanceOf(self.account)

    def balanceEnergyToken(self):
        return b4p.EnergyToken.balanceOf(self.account)






    