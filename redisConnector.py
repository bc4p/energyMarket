import redis
import json
import b4p

if not b4p.started():
    b4p.init()
    b4p.Markets.new("main", "admin")
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
p = r.pubsub()

p.psubscribe('*/register_participant')
p.psubscribe('*/response/register_participant')
p.psubscribe('external-aggregator//*/response/batch_commands')
p.psubscribe('external-aggregator//*/events/all')
# p.psubscribe('*')

print("\nredis connector is listening for market events...\n")


## EVENTS
def handle_registration(event):
    data = json.loads(event["data"])
    asset_id = data["device_uuid"]
    account_id = data["transaction_id"]
    new_prod_asset = b4p.ProducingAssets.new(asset_id, account_id, "main")
    new_cons_asset = b4p.ConsumingAssets.new(asset_id, account_id, "main")

def handle_command_event(event):
    data = json.loads(event["data"])
    responses = data["responses"]
    for account in responses:
        commands = responses[account]
        for command in commands:
            if command["command"] == "bid":
                handle_bid_event(account, json.loads(command["bid"]))

            elif command["command"] == "offer":
                handle_offer_event(account, json.loads(command["offer"]))
            
def handle_account_registration(event):
    data = json.loads(event["data"])
    new_account = b4p.Accounts.new(data["transaction_id"])


def handle_all_market_events(event):
    data = json.loads(event["data"])
    if(data["event"] == "market"):
        pass#handle_slot_event(data["grid_tree"])
    elif(data["event"] == "tick"):
        pass#handle_tick_event(data)
    elif(data["event"] == "trade"):
        handle_trade_event(data)
    elif(data["event" == "finish"]):
        handle_finish_event(data)

    

## SUB-EVENTS
def handle_slot_event(grid_tree):
    #print("#####SLOT EVENT######")
    for node_id in grid_tree:
        node = grid_tree[node_id]
        get_node_info(node, node_id)

def get_node_info(node, node_id):
    if "children" in node:
        children = node["children"]
        for child_node_id in children:
            node = children[child_node_id]
            get_node_info(node, child_node_id)
            return
    if "asset_bill" in node:
        asset_bill = node["asset_bill"]
        if "bought" in asset_bill and asset_bill["bought"] > 0:
            energy_bought = asset_bill["bought"]
        if "sold" in asset_bill and asset_bill["sold"] > 0:
            energy_sold = asset_bill["sold"]
        return 


def handle_tick_event(data):
    pass

def handle_trade_event(data):
    print("\n\n\n\n************************************************************** TRADE EVENT **************************************************************")
    trades = data["trade_list"]
    for trade in trades:
        bid_id = trade["bid_id"]
        asset = b4p.ProducingAssets[trade["asset_id"]]
        price = trade["trade_price"]
        amount = trade["traded_energy"]
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



## OTHER
def handle_all(event):
    pass
    




while True:
    for i in p.listen():
        pattern = i["pattern"]
        if pattern == '*/register_participant':
            handle_account_registration(i)    
        if pattern == '*/response/register_participant':
            handle_registration(i) 
        if pattern == 'external-aggregator//*/response/batch_commands':
            handle_command_event(i) 
        if pattern == 'external-aggregator//*/events/all':
            handle_all_market_events(i)
        if pattern == '*':
            handle_all(i)

