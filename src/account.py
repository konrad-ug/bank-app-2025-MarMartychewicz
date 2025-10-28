class Account:
    express_outgoing_fee = 0

    def __init__(self):
        self.history = []

    def is_number(self, number):
        try:
            val = int(number)
            return True
        except ValueError:
            return False

    def incoming(self, sum):
        if self.is_number(sum):
            self.balance += sum
        else:
            return 'error: incoming sum is not a number'

    def outgoing(self, sum):
        if self.is_number(sum):
            if self.balance >= sum:
                self.balance -= sum
            else:
                return 'error: Not enough funds to complete transaction'
        else:
            return 'error: outgoing sum is not a number'

    def express(self, sum):
        if self.is_number(sum):
            if self.balance >= self.express_outgoing_fee:
                self.balance -= (self.express_outgoing_fee+sum)
            else:
                return 'error: Not enough funds to complete transaction'
        else:
            return 'error: outgoing sum is not a number'