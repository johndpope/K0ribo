import csv
import datetime as datetime
import json
import time
from datetime import datetime
from getpass import _raw_input

from bittrex import Bittrex
from _thread import start_new_thread, allocate_lock

#classes
class Hist_element:
    def __init__(self, id, amount, price, ts):
        self.id = id
        self.amount = amount
        self.price = price
        self.ts = ts

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return str(self.__dict__)

class Out_element1:
    def __init__(self,minutes, price, trans_amount, coin_amount, change_sm, change_md, change_lg, t0_price):
        self.minutes = minutes
        self.price = price
        self.trans_amount = trans_amount
        self.coin_amount = coin_amount
        self.change_sm = change_sm
        self.change_md = change_md
        self.change_lg = change_lg
        self.t0_price = t0_price

    def getIterable(self):
        return [self.minutes, self.trans_amount, self.coin_amount, self.change_sm, self.change_md, self.change_lg, self.akt_price]

#settings
CHANGE_SM = 5*60 #seconds
CHANGE_MD = 15*60 #seconds
CHANGE_LG = 30*60 #seconds
HISTORY = 60*60 #size of history store in seconds
OFFSET = 30*60 #time for future prediction
#vars + init
my_bitterx = Bittrex(None, None)
history_store = [] #storage for history
markets = json.load(open("markets.json",'r'))
for market in markets:
    history_store.append({ "flag": False, "market": market, "history":[]})
lock = allocate_lock()

#extract markethistory
def hist_fetch(a):
    global my_bitterx, history_store, markets
    print("Thread 1 started")
    while True:
        for store in history_store:
            akt_hist = Bittrex.get_market_history(my_bitterx,store["market"],200)["result"] #get history for every market
            akt_hist.reverse()
            for element in akt_hist:
                try:
                    element = Hist_element(element['Id'],element['Quantity'],element['Price'],datetime.strptime(element['TimeStamp'],'%Y-%m-%dT%H:%M:%S.%f')) #get required fields
                    #print(element)
                except ValueError:
                    element = Hist_element(element['Id'],element['Quantity'],element['Price'],datetime.strptime(element['TimeStamp'],'%Y-%m-%dT%H:%M:%S')) #get required fields
                lock.acquire()
                if element not in store["history"]:
                    store["history"].append(element)
                    #print(store["market"] + " added: "+str(element))
                lock.release()
            lock.acquire()
            while datetime.utcnow().timestamp() - store["history"][0].ts.timestamp() > HISTORY:
                #print(str(history_store[i][0]))
                #print((history_store[i][0].ts.timestamp()-datetime.utcnow().timestamp())/60)
                store["flag"] = True
                store["history"].pop(0)
            #print((datetime.utcnow().timestamp()-history_store[i][len(history_store[i])-1].ts.timestamp())/60)
            #print((datetime.utcnow().timestamp()-history_store[i][0].ts.timestamp())/60)
            lock.release()
            print(len(store["history"]))
        time.sleep(20)

def brain_result(b):
    global history_store
    print("Thread 2 started")
    for element in history_store:
        element["Flag"] = False
    while True:
        print("I am working")
        for store in history_store:
            if store["flag"]:  #true if history goes back 30 minutes
                print("Output steht bevor")
                coin_count, transactions, changesm, changemd, changelg = 0, 0, 0, 0, 0
                akt_value = my_bitterx.get_ticker(store["market"])['result']['Last']
                offset_value
                for element in store["history"]:
                    if (datetime.utcnow().timestamp() - element.ts.timestamp()) < OFFSET:
                        offset_value = element.price
                akt_time = datetime.utcnow().hour * 60 + datetime.utcnow().minute
                changelg = offset_value - store["history"][0].price
                lock.acquire()
                for counter, element in enumerate(store["history"]):
                    time_diff = datetime.utcnow().timestamp() - element.ts.timestamp()
                    if time_diff < (CHANGE_SM + OFFSET) and time_diff > OFFSET:
                        if changesm == 0:
                            changesm = (offset_value - element.price) / element.price
                        transactions += 1
                        coin_count += element.amount
                    else:
                        if time_diff < (CHANGE_MD + OFFSET) and time_diff > OFFSET and changemd == 0:
                            changemd = (offset_value - element.price) / element.price
                lock.release()
                out = Out_element1(akt_time, offset_value, transactions, coin_count, changesm, changemd, changelg, akt_value)
                with open("brain_out.csv", "a") as brain_out:
                    csv_writer = csv.writer(brain_out, delimiter=';', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow(out.getIterable())
                    print("New Output")
        time.sleep(1*60)


start_new_thread(hist_fetch,(1,))
time.sleep(60*30)
start_new_thread(brain_result,(2,))
c = _raw_input("Eingabe.")
