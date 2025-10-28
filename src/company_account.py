from src.account import Account

class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        self.balance = 0
        self.express_cost = 5
    
    def express(self, sum):
        return super().express(sum, self.express_cost)

    def is_nip_valid(self, nip):
        if len(nip) == 10:
            return True
        else: return False