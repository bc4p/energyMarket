import redis
import json
#import b4p

#if not b4p.started():
#    b4p.init()
r = redis.StrictRedis(host='localhost', port=6379, db=0)
p = r.pubsub()
p.psubscribe('*/register_participant')
p.psubscribe('*/response/register_participant')



def handle_registration(data):
    data = json.loads(data.decode())
    #print(data)
    print(data["transaction_id"])
    #b4p.Accounts.new(data["transaction_id"])
def handle_account_registration(data):
    data = json.loads(data.decode())
    #print(data)
    #print(f"registre account {data}")

while True:
    for i in p.listen():
        #print(i)
        patter = i["pattern"]
        if patter == b'*/register_participant':
            handle_account_registration(i["data"])    
        if patter == b'*/response/register_participant':
            handle_registration(i["data"]) 
