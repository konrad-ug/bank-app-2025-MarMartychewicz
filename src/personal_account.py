from src.account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 50 if (self.is_promo_code_valid(promo_code) and self.is_required_age(pesel)) else 0
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"