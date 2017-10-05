import json
import time
import sys
import os
import urllib.request
from bittrex import Bittrex

#classes
class Hist_element:
    def __init__(self, id, amount, price, ts):
        self.id = id
        self.amount = amount
        self.price = price
        self.ts = ts

class Out_element:
    def __init__(self):
#settings
CHANGE1 = 5 #minuten
CHANGE2 = 15 #minuten
CHANGE3 = 30 #minuten
HISTORY = 60 #dauer die gespeichert wird(30 mins past, 30 mins future)

#vars + init
my_bitterx = Bittrex(None, None)
history_stor = [] #storage for history
markets = json(open("markets.json"))



history = Bittrex.get_market_history(my_bitterx,'BTC-NEO',1)["result"]
print(len(history))
with open("history.json",'w') as file_history:
    file_history.write(str(history))
file_trading = open('trading.json', 'r')
json_trading = json.load(file_trading)
file_trading.close()
while True:
    for market in json_trading:
        tick = str(my_bitterx.get_ticker(market).get('result')['Last'])+";"+str(time.time())
        with open(market+'.json','a') as file_ouput_tick:
            file_ouput_tick.write("\n"+str(tick))
    time.sleep(10)

