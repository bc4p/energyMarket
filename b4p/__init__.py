from brownie import *
import sys, os


has_started = False

def init():
    global has_started
    global p
    global zero_address
    global url
    global EURS

    has_started = True
    project_path = os.path.dirname(os.path.realpath(__file__))+"\\b4p-contracts"
    p = project.load(project_path)
    p.load_config()
    network.connect('mainnet-fork')
    

    EURS = config["networks"][network.show_active()].get("eurs")
    zero_address = "0x0000000000000000000000000000000000000000"
    url = "https://exampleURL.com"
    from .energyToken import EnergyToken
    from .market import Market
    from .producingAsset import ProducingAsset
    from .consumingAsset import ConsumingAsset

    from .accounts import Accounts
    from .registry import Registry



    globals()["Accounts"] = Accounts()
    globals()["EnergyToken"] = EnergyToken()
    globals()["Registry"] = Registry()
    globals()["Market"] = Market()
    globals()["ProducingAsset"] = ProducingAsset()
    globals()["ConsumingAsset"] = ProducingAsset()

    

def started():
    return has_started


