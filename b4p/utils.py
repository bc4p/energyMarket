PRINT_EVENTS = ["Match", "TransferSingle", "Transfer"]
import json 

def print_transaction_events(tx):
    print_bool = False
    print_message = f'\n°°°°°°°°°°°°°°°°°°°°°°°°°°° BLOCKCHAIN EVENTS °°°°°°°°°°°°°°°°°°°°°°°°°°°\n'
    events = tx.events
    for event in events:
        name = event.name
        if name in PRINT_EVENTS:
            print_bool = True
            print_message+= f'\n    --------{name}--------\n'
            for items in event:
                for item in items:
                    print_message+= f'        {item}: {items[item]}\n'
            print_message+= '    ------------------------'
    print_message+=f'\n°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°\n'
    
    if print_bool:
        print(print_message)

def  fund_account(account):
    import requests
    import json
    url = "https://bc4p.nowum.fh-aachen.de/faucet/api/add_key"
    payload = json.dumps({
    "public_key": account.address
    })
    headers = {'content-type': 'application/json',}

    initial_balance = account.balance()
    response = requests.request("POST", url, headers=headers, data=payload)
    response_message = json.loads(response.text)["Message"]
    response_status_code = response.status_code
    if response_status_code == 200:
        new_balance = account.balance()
        while initial_balance == new_balance:
            new_balance = account.balance()


    else:
        raise Exception(f"something went wrong while requesting funds from faucet | code:{response_status_code} message:{response_message}")


