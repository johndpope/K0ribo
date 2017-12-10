import csv
import threading
import time
from datetime import datetime

from bittrex import Bittrex


class Out_element:
    def __init__(self,minutes, price, volume, change_sm, change_md, change_lg, buy):
        self.minutes = minutes
        self.price = "{:.16f}".format(float(price))
        self.volume = volume
        self.change_sm = "{:.16f}".format(float(change_sm))
        self.change_md = "{:.16f}".format(float(change_md))
        self.change_lg = "{:.16f}".format(float(change_lg))
        self.buy = buy

    def getIterable(self):
        return [self.minutes, self.price, self.volume, self.change_sm, self.change_md, self.change_lg, self.buy]



class BrainDataGen(threading.Thread):
    def __init__(self, stores, settings):
        self.stores = stores
        self.settings = settings
        self.my_bittrex = Bittrex(None, None)
        threading.Thread.__init__(self)

    def run(self):
        print("Thread 2 started")
        try:
            time.sleep(60*60)
            for element in self.stores:
                element.lock.acquire()
                element.flag = False
                element.lock.release()
        except:
            with open("log.txt", "a") as log:
                log.write("Fehler vor Start des Output Generators")
        while True:
            print("I am working")
            for store in self.stores:
                try:
                    if store.flag:  #true if history goes back 30 minutes
                        print("Output steht bevor: "+store.market)
                        coin_count, transactions, changesm, changemd, changelg = 0, 0, 0, 0, 0 #Variablen initialisieren
                        akt_value = self.my_bittrex.get_ticker(store.market)['result']['Last'] #History-Daten von Bittrex holen.
                        offset_value = 0 #Offset-Preis t=0
                        store.lock.acquire()
                        for element in store.history: #start: t-30
                            if (datetime.utcnow().timestamp() - element.ts.timestamp()) < self.OFFSET: #Wenn Zeitpunkt näher als t=0 (also z.B: t+1)
                                offset_value = element.price
                        akt_time = datetime.utcnow().hour * 60 + datetime.utcnow().minute #aktuelle Zeit in Minuten
                        changelg = (offset_value - store.history[0].price)/ store.history[0].price #Prozentuale Änderung von OFFSET(t=0)+CHANGE_LG(t-30) => Wert der am weitesten in der Vergangenheit liegt.
                        for element in store.history:#start: t-30
                            time_diff = datetime.utcnow().timestamp() - element.ts.timestamp()#Zeitunterschied zwischen ELement und jetzt
                            if time_diff < self.OFFSET: #Wenn Wert näher an Gegenwart als t=0
                                break
                            if time_diff < (self.CHANGE_SM + self.OFFSET): #Wenn Element zwischen t=0 und t-5 liegt
                                transactions += 1#Zahl der Transaktionen zwischen t=0 und t-5
                                coin_count += element.amount#Zahl der gehandelten Coins zwischen t=0 und t-5
                                if changesm == 0: #Wenn Element das erste mal zwischen t=0 und t-5 liegt
                                    changesm = (offset_value - element.price) / element.price #Prozentuale Änderung von OFFSET(t=0)+CHANGE_SM(t-5)
                                    print("SM gesetzt")
                            else:
                                if time_diff < (self.CHANGE_MD + self.OFFSET) and changemd == 0:#Wenn Element das erste mal zwischen
                                    changemd = (offset_value - element.price) / element.price
                                    print("MD gesetzt")
                        store.lock.release()
                        out = Out_element1(akt_time, offset_value, transactions, coin_count, changesm, changemd, changelg, akt_value)
                        with open("brain_out.csv", "a") as brain_out:
                            csv_writer = csv.writer(brain_out, delimiter=';', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            csv_writer.writerow(out.getIterable())
                            print("New Output")
                        #for element in store.history:
                            #with open("debug.txt", "a") as log:
                                #log.write(str(element)+"\n")

                        #with open("debug.txt", "a") as log:
                            #log.write("=========================================\n")
                except Exception as e:
                    with open("log.txt", "a") as log:
                        log.write("==============================================================================\n")
                        log.write(str(datetime.timestamp()))
                        log.write("Fehler beim Erstellen von Output: " + store.market + "\n")
                        log.write(str(e)+"\n")
                        log.write("==============================================================================\n")
            time.sleep(5 * 60)
