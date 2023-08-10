import redis
import json
import b4p
import ast
import time

ACCOUNTS = {
    "account1":["B04"],
    "account2":["B05a", "B06"],
    "account3":["B08"],
    "account4":["B09"],
    "account5":["B10"],
    "account6":["B11"],
    "account7":["B13"],
    "account8":["B15"],
    "account9":["B17"],
    "account10":["B21"],
    "account11":["B22"],
    "account12":["B23"],
    "account13":["B28"],
    "account14":["B31"],
    "account15":["B34"],
    "account16":["B36"],
    "account17":["B41"],
    "account18":["B42"],
    "account19":["B52"],
    "account20":["B529"],
    "account21":["Market Maker"],
    "account22":["Liege"]
}

if not b4p.started():
    account = b4p.init_account('mainnet-fork')
    b4p.init(account)


b4p.Markets.new("main", "admin")
for account in ACCOUNTS:
    account_assets = ACCOUNTS[account]
    eth_account = b4p.Accounts.new(account)
    eth_account.fundEURS()
    
    b4p.SoulBound.createIdentity(eth_account, "name")
    for asset in account_assets:
        b4p.ProducingAssets.new(asset, eth_account, "main")
        b4p.ConsumingAssets.new(asset, eth_account, "main")
        print(f"retreiving assets for {eth_account}:\n")
        print(b4p.SoulBound.assets(eth_account.address))
    



r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
p = r.pubsub()
p.psubscribe('market/*/notify_event')
p.psubscribe('DEVICES UNIQUE NAMES')
p.psubscribe('*/market_event')
p.psubscribe('*/market_event_reponse')
p.psubscribe('*/OFFER')
p.psubscribe('*/OFFER/response')
p.psubscribe('*')
"""
registry user devide, 
soulbound token has user name.

"""
ASSETS_REGISTERED = False
print("\nredis connector is listening for market events...\n")

            
def handle_account_registration(event):
    global ASSETS_REGISTERED 
    if ASSETS_REGISTERED:
        return
    areas = ast.literal_eval(event["data"])

    for asset_info in areas:
        print(f'creating account for {asset_info["name"]}')
        b4p.Accounts.new(asset_info["uuid"])
        b4p.ProducingAssets.new(asset_info["uuid"], asset_info["uuid"], "main")
        b4p.ConsumingAssets.new(asset_info["uuid"], asset_info["uuid"], "main")
    ASSETS_REGISTERED = True


    




def handle_tick_event(data):
    grid_tree = data['grid_tree']
    for node_id in grid_tree:
        market_fee = grid_tree[node_id]["last_market_fee"]
        current_market_fee = b4p.Markets['main'].fee()
        if market_fee != current_market_fee:
            b4p.Markets['main'].set_fee(market_fee)
            # change_current_market_fee = b4p.Markets['main'].fee()
            # print("change_current", change_current)
        print("###")




def handle_trade_event(data):
    print("\n\n\n\n************************************************************** TRADE EVENT **************************************************************")
    trades = data["trade_list"]
    for trade in trades:
        bid_id = trade["bid_id"]
        asset = b4p.ProducingAssets[trade["asset_id"]]
        price = trade["trade_price"]
        amount = trade["traded_energy"]
        if bid_id != "None":
            asset.acceptBid(price, amount, bid_id)
        
    print("\n\n\n\n*****************************************************************************************************************************************")

def handle_finish_event(data):
    pass

def handle_bid_event(account, bid):
    asset = b4p.ConsumingAssets[account]
    asset.createBid(bid["price"], bid["energy"], bid["id"])
    print(f'\nnew BID --> price: {bid["price"]}  energy: {bid["energy"]}\n')



def handle_offer_event(account, offer):
    asset = b4p.ProducingAssets[account]
    asset.createOffer(offer["price"], offer["energy"], offer["id"])
    print(f'\nnew OFFER --> price: {offer["price"]}  energy: {offer["energy"]}\n')


def handle_market_event(event):
    event_data = json.loads(event["data"])
    trade = json.loads(event_data['kwargs']["trade"])
    trade_id = trade["id"]
    offer_bid = json.loads(trade["offer_bid"])
    offer_bid_id = offer_bid["id"]
    
    price = offer_bid["price"]
    energy = offer_bid["energy"]
    rate = offer_bid["energy_rate"]
    seller_id = trade["seller_id"]
    buyer_id = trade["buyer_id"]
    traded_energy = trade["traded_energy"]
    trade_price = trade["trade_price"]
    rate = trade_price/traded_energy

    

    producing_asset = b4p.ProducingAssets[seller_id]
    consuming_asset = b4p.ConsumingAssets[buyer_id]
    print(f"producing asset: {producing_asset}")
    print(f"consuming_asset: {consuming_asset}")

    consuming_asset.createBid(price, energy, trade_id,)
    producing_asset.acceptBid(price, energy, trade_id, seller_id, buyer_id)
    b4p.logger.log_dictionary({"seller_id":seller_id, "buyer_id":buyer_id, "traded_energy":traded_energy, "traded_price":trade_price, "traded_rate":rate, "bid_id":offer_bid_id, "timestamp":time.time()}, "trades")

## OTHER
def handle_all(event):
    #print(event)
    pass




# def handle_market_offer_fee(event)




while True:
    for i in p.listen():
        pattern = i["pattern"]
        # if pattern == 'DEVICES UNIQUE NAMES':
        #     handle_account_registration(i)    
        if pattern == 'market/*/notify_event':
            handle_market_event(i) 
      

