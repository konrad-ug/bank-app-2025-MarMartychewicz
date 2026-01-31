from account import Account
import requests, json
from datetime import date

class CompanyAccount(Account):
    express_outgoing_fee = 5.0

    def __init__(self, company_name, nip):
        self.company_name = company_name
        #self.nip = nip if self.is_nip_len_valid(nip) else "Invalid"
        self.nip = nip

        if self.is_nip_len_valid(nip):
            result = self.nip_api_check(nip)
            if result == [True, True]:
                print('Status VAT jest czynny')
            elif result == [True, False]:
                print('Status VAT nie jest czynny')
            else:
                raise ValueError('Company not registered!!')

        self.balance = 0
        self.express_cost = 5
        self.history = []
    
    def express(self, sum):
        return super().express(sum)

    def is_nip_len_valid(self, nip):
        if len(str(nip)) == 10:
            return True
        else: return False
    
    def nip_api_check(self, nip):
        NIP_TEST_URL = 'https://wl-api.mf.gov.pl'

        cdate = date.today().isoformat()  # YYYY-MM-DD
        url = f'{NIP_TEST_URL}/api/search/nip/{nip}?date={cdate}'

        data = requests.get(url).json()
        if data.get("code") == "WL-115":
            return [False, False]

        try:
            result = data["result"]["subject"]["statusVat"] == "Czynny"
        except Exception:
            result = False

        return [True, result]

    def sufficient_balance(self, amount):
        return True if (self.balance >= amount) else False
    
    def zus_paid(self):
        return True if (-1775 in self.history) else False

    def submit_for_loan(self, amount):
        if (self.sufficient_balance(amount) and self.zus_paid()):
            self.balance += amount
            return True
        else: return False