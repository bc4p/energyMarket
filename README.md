# b4p package

## setup

clone this repository with its submodules by calling

```
git clone --recurse-submodules https://github.com BC4P/energyMarket.git
```  
Next, locate the .env file [here](energyMarket/b4p/b4p-contracts/.env) and fill put the api keys for infura and etherscan. The api keys will be used to connect to the blockchain through an infura node and pull down external contracts through the etherscan API. 

Only when the api keys are in the .env file go to the root directory and istall the package by running

```
cd energyMarket
pip install .
```



