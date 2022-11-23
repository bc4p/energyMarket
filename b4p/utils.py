PRINT_EVENTS = ["Match", "TransferSingle", "Transfer"]

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
