import threading

from datetime import datetime
import time
import array
import Bittrex
from pymongo import MongoClient

class Store(threading.Thread):
    def __init__(self, exchange, market, HISTORY_LEN):
        self.exchange = exchange
        self.market = market
        self.my_bittrex = Bittrex.Bittrex(None, None, 1, Bittrex.using_requests, Bittrex.API_V1_1)
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
            ts, volume, openBuyOrders, openSellOrders, price = 0, 0, 0, 0, 0
            try:
                summary = self.my_bittrex.get_market_summary(self.market)["result"]
                ts = summary["TimeStamp"]
                volume = summary["Volume"]
                openBuyOrders = summary["openBuyOrders"]
                openSellOrders = summary["openSellOrders"]
                price = summary["Last"]
            except Exception as e:
                    with open("log.txt", "a") as log:
                        log.write("***************************************************\n")
                        log.write(str(datetime.timestamp()))
                        log.write("Fehler beiHistory Abfrage: " + self.market + "\n")
                        log.write(str(e)+"\n")
                        log.write("***************************************************\n")


    def removeOld(self):
        if len(self.history) > 0:
            self.lock.acquire()
            while (datetime.utcnow().timestamp() - self.history[0].ts.timestamp()) > self.HISTORY_LEN:
                self.history.pop(0)
                self.flag = True
                if len(self.history) == 0:
                    break
            self.lock.release()
