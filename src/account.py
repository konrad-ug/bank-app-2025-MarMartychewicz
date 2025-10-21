class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 50 if (self.is_promo_code_valid(promo_code) and self.is_required_age(pesel)) else 0
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
    
    def is_pesel_valid(self, pesel):
        if len(pesel) == 11 and pesel.isdigit():
            return True
        else:
            return False
    
    def is_promo_code_valid(self, promo_code):
        if promo_code is None:
            return False
        if promo_code[:5] == "PROM_" and len(promo_code) == 8:
            return True
        else:
            return False

    def is_required_age(self, pesel):
        if int(pesel[2:4]) > 12:
            return True
        elif int(pesel[0:2]) >= 60:
            return True
        else:
            return False
    
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

