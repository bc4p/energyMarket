from b4p import p
from brownie.network import accounts

class Accounts:
    def __init__(self):
        self.accounts = {}
        self.accounts["admin"] = accounts[0]
        self.counter = 1
        pass

    def __getitem__(self, name):
        return self.accounts[name]


    def new(self, name):
        self.accounts[name] = accounts[self.counter]
        self.counter += 1



    