from . import url, p
class MockToken():
        def __init__(self):
            from . import Accounts
            print("URL",url)

            self.mockToken = p.MockEursToken.deploy(url, {"from": Accounts["admin"]})

        def __str__(self):
            return self.mockToken.__str__()

        def __repr__(self):
            return self.mockToken.__repr__()

        def balanceOf(self, address):
            return self.mockToken.balanceOf(address, 1)