class Account:
    def __init__(self, currency, balance, available, pending):
        self.currency = currency
        self.balance = balance
        self.available = available
        self.pending = pending

    def __eq__(self, other):
        return self.currency == other.currency
