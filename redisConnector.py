import redis
import json
import b4p

if not b4p.started():
    b4p.init()
    b4p.Markets.new("main", "admin")

r = redis.StrictRedis(host='localhost', port=6379, db=0)
p = r.pubsub()

p.psubscribe('*/register_participant')
p.psubscribe('*/response/register_participant')
p.psubscribe('external-aggregator//*/response/batch_commands')
p.psubscribe('external-aggregator//*/events/all')


def handle_registration(event):
    # print(event)
    # print()

    data = json.loads(event["data"].decode())
    asset_id = data["device_uuid"]
    account_id = data["transaction_id"]
    b4p.ProducingAssets.new(asset_id, account_id, "main")
    b4p.ConsumingAssets.new(asset_id, account_id, "main")

def handle_trade(event):
    #print(event)
    #print()
    data = json.loads(event["data"].decode())
    responses = data["responses"]
    for account in responses:
        commands = responses[account]
        for command in commands:
            if command["command"] == "bid":
                asset = b4p.ConsumingAssets[account]
                bid =  json.loads(command["bid"])
                asset.createBid(bid["price"], bid["energy"])

            elif command["command"] == "offer":
                asset = b4p.ProducingAssets[account]
                offer =  json.loads(command["offer"])
                asset.createOffer(offer["price"], offer["energy"])

            

def handle_account_registration(event):
    #print(event)
    #print()
    data = json.loads(event["data"].decode())
    b4p.Accounts.new(data["transaction_id"])
    
def handle_all(event):
    print(event)
    print()
    




while True:
    for i in p.listen():
        # print(i)  
        # print()
        patter = i["pattern"]
        if patter == b'*/register_participant':
            handle_account_registration(i)    
        if patter == b'*/response/register_participant':
            handle_registration(i) 
        if patter == b'external-aggregator//*/response/batch_commands':
            handle_trade(i) 
        if patter == b'*':
            handle_all(i)

