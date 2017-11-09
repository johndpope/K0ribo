from getpass import _raw_input

from bittrex import Bittrex

from Store import Store
from Brain_In_Gen import BrainDataGen


#settings

CHANGE_SM = 5*60 #seconds
CHANGE_MD = 15*60 #seconds
CHANGE_LG = 30*60 #seconds
HISTORY = 60*60 #size of history store in seconds
OFFSET = 30*60 #time for future prediction

my_bittrex = Bittrex(None, None)
bit_markets = my_bittrex.get_market_summaries()["result"]
stores = []
for market in bit_markets:
    if str(market["MarketName"]).startswith("BTC"):
        stores.append(Store(market["MarketName"], market["BaseVolume"], OFFSET))

stores = sorted(stores, key=lambda store: store.MARKET_VOLUME, reverse=True)[:20]

for store in stores:
    store.start()

brain_in_gen = BrainDataGen(stores, OFFSET, CHANGE_SM, CHANGE_MD, CHANGE_LG)
brain_in_gen.start()


c = _raw_input("Eingabe.")
