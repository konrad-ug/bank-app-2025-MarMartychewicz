from src.account import Account


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