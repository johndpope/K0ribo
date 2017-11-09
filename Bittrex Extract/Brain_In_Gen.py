import csv
import threading
import time
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
        return [self.minutes, self.price, self.trans_amount, self.change_sm, self.change_md, self.change_lg, self.t0_price]

class BrainDataGen(threading.Thread):
    def __init__(self, stores, OFFSET, CHANGE_SM, CHANGE_MD, CHANGE_LG):
        self.stores = stores
        self.OFFSET = OFFSET
        self.CHANGE_SM = CHANGE_SM
        self.CHANGE_MD = CHANGE_MD
        self.CHANGE_LG = CHANGE_LG
        self.my_bittrex = Bittrex(None, None)
        threading.Thread.__init__(self)

    def run(self):
        print("Thread 2 started")
        for element in self.stores:
            element.flag = False
        time.sleep(60*60)
        while True:
            print("I am working")
            for store in self.stores:
                if store.flag:  #true if history goes back 30 minutes
                    print("Output steht bevor: "+store.market)
                    coin_count, transactions, changesm, changemd, changelg = 0, 0, 0, 0, 0 #Variablen initialisieren
                    akt_value = self.my_bittrex.get_ticker(store.market)['result']['Last'] #History-Daten von Bittrex holen.
                    offset_value = 0 #Offset-Preis t=0
                    store.lock.acquire()
                    for element in store.history:
                        if (datetime.utcnow().timestamp() - element.ts.timestamp()) < self.OFFSET: #Wert vor OFFSET(t=0) minuten
                            offset_value = element.price
                    akt_time = datetime.utcnow().hour * 60 + datetime.utcnow().minute #aktuelle Zeit in Minuten
                    changelg = (offset_value - store.history[0].price)/ store.history[0].price #Prozentuale Änderung von OFFSET(t=0)+CHANGE_LG(t-30) => Wert der am weitesten in der Vergangenheit liegt.
                    for element in store.history:
                        time_diff = datetime.utcnow().timestamp() - element.ts.timestamp()
                        if time_diff > self.OFFSET: #Wenn Wert weiter in der Vergangenheit als t=0
                            if time_diff < (self.CHANGE_SM + self.OFFSET): #Wenn Wert kleiner als t-5 ist
                                transactions += 1
                                coin_count += element.amount
                                if changesm == 0: #Wenn er das erste mal kleiner ist
                                    changesm = (offset_value - element.price) / element.price
                            else:
                                if time_diff < (self.CHANGE_MD + self.OFFSET) and changemd == 0:#Wenn Wert kleiner als t-15 ist
                                    changemd = (offset_value - element.price) / element.price
                    store.lock.release()
                    out = Out_element1(akt_time, offset_value, transactions, coin_count, changesm, changemd, changelg, akt_value)
                    with open("brain_out.csv", "a") as brain_out:
                        csv_writer = csv.writer(brain_out, delimiter=';', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(out.getIterable())
                        #print("New Output")
            time.sleep(5 * 60)
