from bittrex import Bittrex
import threading
import json
from account import Account
import time

class Wallet(threading.Thread):

    def __init__(self, key, secret):
        self.lock = threading.Lock()
        self.my_bittrex = Bittrex(key, secret)
        self.wallet=[]
        threading.Thread.__init__(self)

    def __contains__(self, item):
        if type(item) is Account:
            if self.wallet.__contains__(item):
                return True
        if type(item) is str:
            print(item)
            for account in self.wallet:
                print(account.currency)
                if account.currency == item:
                    return True
        return False

    def __getitem__(self, item):
        for account in self.wallet:
            if account.currency == item:
                return account

    def run(self):
        tmp_wallet = self.my_bittrex.get_balances()["result"]
        self.lock.acquire()
        self.wallet = []
        self.lock.release()
        while True:
            markets = self.my_bittrex.get_markets()["result"]
            tmp_wallet = self.my_bittrex.get_balances()["result"]
            self.lock.acquire()
            self.wallet = []
            for element in tmp_wallet:
                for market in markets:
                    print(str(market))
                    if market["MarketCurrency"] == element["Currency"]:
                        self.wallet.append(Account(element["Currency"], element["Balance"], element["Available"], element["Pending"], market["MinTradeSize"]))
            self.lock.release()
            time.sleep(60)


    def buy(self, account_name, amount, price):
        print("Buying incoming")
        response = self.my_bittrex.buy_limit("BTC-"+account_name, amount, price)
        print(response)

    def sell(self, account_name, amount, price):
        if self.__contains__(account_name):
            print("Selling incoming")
            response = self.my_bittrex.sell_limit("BTC-"+account_name, amount,price)
            print(response)

    def getWallet(self):
        return self.wallet
