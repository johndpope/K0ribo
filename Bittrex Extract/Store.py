import threading

from datetime import datetime
import time
import array
from bittrex import Bittrex


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


class Store(threading.Thread):
    def __init__(self, market, MARKET_VOLUME, HISTORY_LEN):
        self.market = market
        self.MARKET_VOLUME = MARKET_VOLUME
        self.my_bittrex = Bittrex(None, None)
        self.history = []
        self.flag = False
        self.lock = threading.Lock()
        self.HISTORY_LEN = HISTORY_LEN
        threading.Thread.__init__(self)

    def __str__(self):
        return str(self.__dict__)

    def getHistory(self) -> array:
        return self.history

    def run(self):
        while True:
            try:
                new_history = self.my_bittrex.get_market_history(self.market, 200)["result"]
                if new_history:
                    new_history.reverse()
                    self.lock.acquire()
                    for element in new_history:
                        try:
                            element = Hist_element(element['Id'], element['Quantity'], element['Price'],
                                                   datetime.strptime(element['TimeStamp'],
                                                                     '%Y-%m-%dT%H:%M:%S.%f'))  # get required fields
                            # print(element)
                        except ValueError:
                            element = Hist_element(element['Id'], element['Quantity'], element['Price'],
                                                   datetime.strptime(element['TimeStamp'],
                                                                    '%Y-%m-%dT%H:%M:%S'))  # get required fields
                        if element not in self.history:
                            self.history.append(element)  # add History Element into the Store
                    #print(self.getMarket() + ": " + str(len(self.history)))
                    self.lock.release()
                    self.removeOld()
                    print("Anfrage Abgeschlossen: "+self.market)
                    time.sleep(5)
            except:
                print("Fehler bei History-abfrage: "+self.market)

    def removeOld(self):
        if len(self.history) > 0:
            self.lock.acquire()
            while (datetime.utcnow().timestamp() - self.history[0].ts.timestamp()) > self.HISTORY_LEN:
                self.history.pop(0)
                self.flag = True
                if len(self.history) == 0:
                    break
            self.lock.release()
