from brownie.network import accounts
from . import url, p, Contract, config, network, EXISTING
from .utils import fund_account
class Accounts():
    def __init__(self,account=None, faucet=False):
        self.accounts = {}
        if faucet:
            self.accounts["faucet"] = self.new("faucet", account=Faucet().address)
        else:
            self.accounts["faucet"] = self.new("faucet", account=Faucet(existing=False).address)
        self.accounts["admin"] = self.new("admin", account)
        #cannot do this in FH blockchain
        #EURS.transfer(self.accounts["admin"].address, amount, {"from":  FAUCET})
        

    def __getitem__(self, name):
        path = f"./accounts_keystore/{name}.json"
        account = accounts.load(filename=path, password="no_password")
        return account

    def __str__(self):
        return str(self.accounts)

    def __repr__(self):
        return self.accounts

    def new(self, name, account=None, with_funding=True, password="no_password"):
        if(account == None):
            self.accounts[name] = Account(accounts.add(),name)
        else:
            self.accounts[name] = Account(accounts.at(account, force=True),name)
        if with_funding:
            self.accounts["faucet"].transfer(self.accounts[name].address, "1 ether")
        self.accounts[name].save(password=password)
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
        from . import EursToken
        return EursToken.balanceOf(self.account)

    def balanceEnergyToken(self):
        from . import EnergyToken
        return EnergyToken.balanceOf(self.account)
    
    def balance(self):
        return self.account.balance()

    def save(self, password, overwrite=True):
        self.account.save(filename=f"./accounts_keystore/{self.name}", overwrite=overwrite, password=password)
        


class Faucet(Account):
    def __init__(self, existing=not EXISTING, fund=True):
        if(existing):
            faucet = accounts.add(config["networks"][network.show_active()]["faucet"]["faucet_pk"])
            fund_account(faucet)
        else:
            faucet = accounts.add()
            if network.show_active() == 'development':
                accounts[0].transfer(faucet, "50 ether")

            else:
                fund_account(faucet)
        Account.__init__(self,faucet,"faucet")




    