import csv
import threading

import datetime

from bittrex import Bittrex


class Out_element1:
    def __init__(self,minutes, price, trans_amount, coin_amount, change_sm, change_md, change_lg, t0_price):
        self.minutes = minutes
        self.price = "{:.16f}".format(float(price))
        self.trans_amount = "{:.16f}".format(float(trans_amount))
        self.coin_amount = "{:.16f}".format(float(coin_amount))
        self.change_sm = "{:.16f}".format(float(change_sm))
        self.change_md = "{:.16f}".format(float(change_md))
        self.change_lg = "{:.16f}".format(float(change_lg))
        self.t0_price = "{:.16f}".format(float(t0_price))

    def getIterable(self):
        return [self.minutes, self.price, self.trans_amount, self.coin_amount, self.change_sm, self.change_md, self.change_lg, self.t0_price]

class BrainDataGen(threading.Thread):
    def __init__(self, stores, OFFSET, CHANGE_SM, CHANGE_MD, CHANGE_LG):
        self.stores = stores
        self.OFFSET = OFFSET
        self.CHANGE_SM = CHANGE_SM
        self.CHANGE_MD = CHANGE_MD
        self.CHANGE_LG = CHANGE_LG
        self.my_bittrex = Bittrex(None, None)

    def run(self):
        print("Thread 2 started")
        for element in self.stores:
            element["Flag"] = False
        while True:
            print("I am working")
            for store in self.stores:
                if store["flag"]:  #true if history goes back 30 minutes
                    print("Output steht bevor: "+store["market"])
                    coin_count, transactions, changesm, changemd, changelg = 0, 0, 0, 0, 0
                    akt_value = self.my_bitterx.get_ticker(store["market"])['result']['Last']
                    offset_value = 0
                    for element in store["history"]:
                        if (datetime.utcnow().timestamp() - element.ts.timestamp()) < self.OFFSET:
                            offset_value = element.price
                    akt_time = datetime.utcnow().hour * 60 + datetime.utcnow().minute
                    changelg = offset_value - store["history"][0].price
                    store.lock.acquire()
                    for counter, element in enumerate(store["history"]):
                        time_diff = datetime.utcnow().timestamp() - element.ts.timestamp()
                        if time_diff < (self.CHANGE_SM + self.OFFSET) and time_diff > self.OFFSET:
                            if changesm == 0:
                                changesm = (offset_value - element.price) / element.price
                            transactions += 1
                            coin_count += element.amount
                        else:
                            if time_diff < (self.CHANGE_MD + self.OFFSET) and time_diff > self.OFFSET and changemd == 0:
                                changemd = (offset_value - element.price) / element.price
                    store.lock.release()
                    out = Out_element1(akt_time, offset_value, transactions, coin_count, changesm, changemd, changelg, akt_value)
                    with open("brain_out.csv", "a") as brain_out:
                        csv_writer = csv.writer(brain_out, delimiter=';', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(out.getIterable())
                        #print("New Output")
            datetime.time.sleep(5 * 60)
