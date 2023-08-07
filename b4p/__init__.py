from brownie import network, project, Contract, config
import sys, os, json

has_started = False


def init_account(network_key='mainnet-fork'):
    global EURS
    global FAUCET
    global zero_address
    global url
    global has_started
    global p


    project_path = os.path.dirname(os.path.realpath(__file__))+"/b4p-contracts"
    p = project.load(project_path)
    p.load_config()
    network.connect(network_key)
    
    

    #EURS = Contract.from_explorer(config["networks"][network.show_active()].get("eurs"))

    zero_address = "0x0000000000000000000000000000000000000000"
    url = "https://exampleURL.com"
    from .logger import DictLogger
    globals()["logger"] = DictLogger("logs")

    from .accounts import Accounts
    globals()["Accounts"] = Accounts()

    from .energyToken import EnergyToken
    globals()["EnergyToken"] = EnergyToken()

    from .eursToken import EursToken
    globals()["EursToken"] = EursToken()

    from .soulbound import SoulBound
    globals()["SoulBound"] = SoulBound()


def init(account=None):
   
   

    #url = "https://exampleURL.com

    '''global EURS


    project_path = os.path.dirname(os.path.realpath(__file__))+"/b4p-contracts"
    p = project.load(project_path)
    p.load_config()
    network_key = 'bc4p-mainnet'
    network.connect(network_key)
    
    with open(os.path.dirname(os.path.realpath(__file__))+'/EURS.abi', 'r') as abi_file:
        eurs_abi_data = json.load(abi_file)

    #EURS = Contract.from_explorer(config["networks"][network.show_active()].get("eurs"))
    EURS = Contract.from_abi("EURSToken", config["networks"][network_key]['eurs'], eurs_abi_data)

    zero_address = "0x0000000000000000000000000000000000000000"
    url = "https://exampleURL.com"'''

    

    from .market import Markets
    from .producingAsset import ProducingAssets
    from .consumingAsset import ConsumingAssets

    from .registry import Registry

    globals()["Registry"] = Registry()
    globals()["Markets"] = Markets()
    globals()["ProducingAssets"] = ProducingAssets()
    globals()["ConsumingAssets"] = ConsumingAssets()
    
    has_started = True

    print(f'\nbronwnie has successfully initialized\nconnnection: {network.show_active()}\n\n')

    

def started():
    return has_started


