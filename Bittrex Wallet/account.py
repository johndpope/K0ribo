class Account:
    def __init__(self, currency, balance, available, pending, minTradeSize):
        self.currency = currency
        self.balance = balance
        self.available = available
        self.pending = pending
        self.minTradeSize = minTradeSize


    def __eq__(self, other):
        return self.currency == other.currency
