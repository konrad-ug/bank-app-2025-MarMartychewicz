from src.account import Account

class CompanyAccount(Account):
    express_outgoing_fee = 5.0

    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        self.balance = 0
        self.express_cost = 5
        self.history = []
    
    def express(self, sum):
        return super().express(sum)

    def is_nip_valid(self, nip):
        if len(str(nip)) == 10:
            return True
        else: return False

    def sufficient_balance(self, amount):
        return True if (self.balance >= amount) else False
    
    def zus_paid(self):
        return True if (-1775 in self.history) else False

    def submit_for_loan(self, amount):
        if (self.sufficient_balance(amount) and self.zus_paid()):
            self.balance += amount
            return True
        else: return False