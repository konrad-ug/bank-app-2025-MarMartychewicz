from src.account import Account

class PersonalAccount(Account):
    express_outgoing_fee = 1.0

    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 50 if (self.is_promo_code_valid(promo_code) and self.is_required_age(pesel)) else 0
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.express_cost = 1
    
    def express(self, sum):
        return super().express(sum)
    
    def is_pesel_valid(self, pesel):
        if len(str(pesel)) == 11 and super().is_number(pesel):
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