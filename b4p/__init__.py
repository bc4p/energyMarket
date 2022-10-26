from brownie import network, project, Contract, config
import sys, os


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
    network.connect('mainnet-fork')
    

    EURS = Contract.from_explorer(config["networks"][network.show_active()].get("eurs"))
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
