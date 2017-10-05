import json
import time
import sys
import os
import urllib.request

import datetime as datetime
from bittrex import Bittrex
from datetime import datetime

#classes
class Hist_element:
    def __init__(self, id, amount, price, ts):
        self.id = id
        self.amount = amount
        self.price = price
        self.ts = ts

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self.__dict__)

class Out_element1:
    def __init__(self,minutes, akt_price, trans_amount, coin_amount, change_sm, change_md, change_lg, fut_price):
        self.minutes = minutes
        self.akt_price = akt_price
        self.trans_amount = trans_amount
        self.coin_amount = coin_amount
        self.change_sm = change_sm
        self.change_md = change_md
        self.change_lg = change_lg
        self.fut_price = fut_price

#settings
CHANGE_SM = 5 #minuten
CHANGE_MD = 15 #minuten
CHANGE_LG = 30 #minuten
HISTORY = 60 #dauer die gespeichert wird(30 mins past, 30 mins future)

#vars + init
my_bitterx = Bittrex(None, None)
history_store = [] #storage for history
markets = json.load(open("markets.json",'r'))
for market in markets:
    history_store.append([])
while True:
    for i in range(0, len(markets)):
        akt_hist = Bittrex.get_market_history(my_bitterx,markets[i],200)["result"] #get history for every market
        akt_hist.reverse()
        for element in akt_hist:
            try:
                element = Hist_element(element['Id'],element['Quantity'],element['Price'],datetime.strptime(element['TimeStamp'],'%Y-%m-%dT%H:%M:%S.%f')) #get required fields
            except ValueError:
                element = Hist_element(element['Id'],element['Quantity'],element['Price'],datetime.strptime(element['TimeStamp'],'%Y-%m-%dT%H:%M:%S')) #get required fields
            if element not in history_store[i]:
                history_store[i].append(element)
        while datetime.utcnow().timestamp() - history_store[i][0].ts.timestamp() > 60*60:
            #print((history_store[i][0].ts.timestamp()-datetime.utcnow().timestamp())/60)
            history_store[i].pop(0)
        #print((datetime.utcnow().timestamp()-history_store[i][len(history_store[i])-1].ts.timestamp())/60)
        #print(len(history_store[i]))
    time.sleep(20)
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

