from src.account import Account
from src.personal_account import PersonalAccount


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0, "Balance is not 0"
        assert account.pesel == "12345678901"
    
    def test_pesel_too_long(self):
        account = Account("John", "Doe", '1234567890111')
        assert account.pesel == "Invalid"
    def test_pesel_too_short(self):
        account = Account("John", "Doe", "123")
        assert account.pesel == "Invalid"
    
    def test_promo_code_valid(self):
        account = Account("John", "Doe", "12345678901", "PROM_abc")
        assert account.balance == 50.0
    def test_promo_code_invalid_format(self):
        account = Account("John", "Doe", "12345678901", "PurM_abc")
        assert account.balance == 0.0
    def test_promo_code_too_long(self):
        account = Account("John", "Doe", "12345678901", "PROM_abcd")
        assert account.balance == 0.0
    def test_promo_code_too_short(self):
        account = Account("John", "Doe", "12345678901", "PROM_ad")
        assert account.balance == 0.0

    def test_person_too_old(self):
        account = Account("John", "Doe", "59115678901", "PROM_abc")
        assert account.balance == 0
    def test_person_age_ok(self):
        account = Account("John", "Doe", "60115678901", "PROM_abc")
        assert account.balance == 50
    def test_person_age_born_after_2000(self):
        account = Account("John", "Doe", "02215678901", "PROM_abc")
        assert account.balance == 50

class TestTransaction:
    def test_incoming_transaction_is_NaN(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming('NaN')
        assert account.balance == 0.0
    def test_incoming_transaction(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming(60.0)
        assert account.balance == 60.0
    def test_outgoing_transaction(self):
        account = Account("John", "Doe", "12345678901", "PROM_abc")
        assert account.balance == 50.0
        account.outgoing(20.0)
        assert account.balance == 30.0
    def test_outgoing_transaction_insufficient_funds(self):
        account = Account("John", "Doe", "12345678901", "PROM_abc")
        assert account.balance == 50.0
        assert account.outgoing(60.0) == 'error: Not enough funds to complete transaction'
        account.outgoing(60.0)
        assert account.balance == 50.0

class TestCompanyAccount:
    def test_company_account_creation(self):
        account = CompanyAccount('CompanyName', '1234567890')
        assert account.c_name == CompanyName
        assert account.nip == '1234567890'
    def test_company_acc_incorrect_nip(self):
        account = CompanyAccount('CompanyName', '123')
        assert account.nip == 'Invalid NIP'
        account2 = CompanyAccount('CompanyName2', '12345678901111111')
        assert account2.nip == 'Invalid NIP'

    def test_company_acc_incoming(self):
        account = CompanyAccount('CompanyName', '1234567890')
        account.incoming(250.0)
        assert account.balance == 250
    def test_company_acc_outgoing(self):
        account = CompanyAccount('CompanyName', '1234567890')
        account.balance = 500.0
        account.outgoing(50)
        assert account.balance == 450
    def test_company_acc_outgoing_insufficient_funds(self):
        account = CompanyAccount('CompanyName', '1234567890')
        account.balance = 10.0
        assert account.outgoing(50) == 'error: Not enough funds to complete transaction'
        account.outgoing(50)
        assert account.balance == 10