from brownie import network, project, Contract, config
import sys, os, json


has_started = False

def init():
    global has_started
    global p
    global zero_address
    global url
    global EURS

    has_started = True

    project_path = os.path.dirname(os.path.realpath(__file__))+"/b4p-contracts"
    p = project.load(project_path)
    p.load_config()
    network.connect('bc4p-mainnet')
    
    with open(os.path.dirname(os.path.realpath(__file__))+'/EURS.abi', 'r') as abi_file:
        eurs_abi_data = json.load(abi_file)

    #EURS = Contract.from_explorer(config["networks"][network.show_active()].get("eurs"))
    EURS = Contract.from_abi("EURSToken", "0xE3feb6eBB7d0B8d0721fEE4842fAE7668259be6e", eurs_abi_data)

    zero_address = "0x0000000000000000000000000000000000000000"
    url = "https://exampleURL.com"
    from .accounts import Accounts
    from .energyToken import EnergyToken
    from .market import Markets
    from .producingAsset import ProducingAssets
    from .consumingAsset import ConsumingAssets

    from .registry import Registry

    globals()["Accounts"] = Accounts()
    globals()["EnergyToken"] = EnergyToken()
    globals()["Registry"] = Registry()
    globals()["Markets"] = Markets()
    globals()["ProducingAssets"] = ProducingAssets()
    globals()["ConsumingAssets"] = ConsumingAssets()

    

def started():
    return has_started
