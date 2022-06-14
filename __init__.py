import b4p
class BC4PBlockchainInterface:
    def __init__(self, market_id, simulation_id=None):
        self.market_id = market_id
        self.simulation_id = simulation_id
        b4p.Markets.new(market_id, "admin")
        print(f"new market created with id: {market_id}")


    def create_new_offer(self, energy, price, seller):
        if not b4p.Accounts[seller+"_account"]:
            print(f"new account created: {seller}_account")
            b4p.Accounts.new(seller+"_account")
        if not b4p.ProducingAssets[seller]:
            print(f"new producing asset created: {seller} for market: {self.market_id}")
            b4p.ProducingAssets.new(seller, seller+"_account", self.market_id)
        return str(uuid.uuid4())

    def cancel_offer(self, offer):
        pass

    def change_offer(self, offer, original_offer, residual_offer):
        pass

    def handle_blockchain_trade_event(self, offer, buyer, original_offer, residual_offer):
        return str(uuid.uuid4()), residual_offer

    def track_trade_event(self, time_slot, trade):
        pass

    def bc_listener(self):
        pass