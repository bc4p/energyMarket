# b4p package

## setup

clone this repository with its submodules by calling

```bash
git clone --recurse-submodules https://github.com/BC4P/energyMarket.git
```

Next, locate the .env file inside [b4p/b4p-contracts/.env](https://github.com/BC4P/b4p-contracts/blob/master/.env) and fill in the api keys for [infura](https://infura.io) and [etherscan](https://etherscan.io/). The api keys will be used to connect to the blockchain through an infura node and pull down external contracts through the etherscan API.

-> this is probably not needed anymore since we are selfhosting our node.

Only when the api keys are in the .env file you can go to the root directory and install the package by running.

```bash
cd energyMarket
pip install -e .
```

:warning:if the .env values are changed the package needs to be reinstalled with the command above:warning:

## Ganache CLI

Install NPM using something like `apt install nodejs` and run
`npm install -g ganache-cli` - which is deprecated in favor of ganache, but brownie still depends on it.

## use

see the [tutorial notebook](tutorial.ipynb) to get familiar with the main functionalities of the package

## BC4P network

This repository relies on brownie and to be able to connect it to the BC4P network, you must add it first:

```bash
brownie networks add BC4P bc4p-mainnet host="https://bc4p.nowum.fh-aachen.de/blockchain" chainid=123321 explorer="https://bc4p.nowum.fh-aachen.de/explorer/api"
brownie account generate admin
brownie account generate testing
```
I had problems that brownie catched up the network from the `brownie-config.yml` directly, therefore this is needed.
The network can be removed with `brownie networks delete bc4p-mainnet`

```python
requests.post('http://bc4p.nowum.fh-aachen.de/faucet/api/add_key', data= {'public_key': PUBLIC_KEY_FROM_BROWNIE})
```

TODO: fix the contract IDs in the config so that the simulation can run on our contracts.
