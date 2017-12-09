from getpass import _raw_input

from bittrex import Bittrex
import json
from Store import Store
from Brain_In_Gen import BrainDataGen


#settings


settings = json.load(open('settings.json'))
my_bittrex = Bittrex(None, None)
bit_markets = my_bittrex.get_market_summaries()["result"]
stores = []
#for market in bit_markets:
#    if str(market["MarketName"]).startswith("BTC"):
#        stores.append(Store(market["MarketName"], market["BaseVolume"], HISTORY))
#
#stores = sorted(stores, key=lambda store: store.MARKET_VOLUME, reverse=True)[:20]

#for store in stores:
#    store.start()

for exchange in settings["exchanges"]:
    for market in exchange["markets"]:
        stores.append(Store(exchange["plattform"], market, settings["HISTORY"]))
brain_in_gen = BrainDataGen(stores, settings)
brain_in_gen.start()


c = _raw_input("Eingabe.")
