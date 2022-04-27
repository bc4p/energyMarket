import b4p

class EnergyToken():
        def __init__(self):
            self.energyToken = b4p.p.EnergyToken.deploy(b4p.url, {"from": b4p.Accounts["admin"]})

        def __str__(self):
            return self.energyToken.__str__()

        def __repr__(self):
            return self.energyToken.__repr__()

        def balanceOf(self, address):
            return self.energyToken.balanceOf(address, 1)