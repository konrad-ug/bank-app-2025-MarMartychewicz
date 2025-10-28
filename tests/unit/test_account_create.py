from src.personal_account import personalAccount


class TestAccount:
    def test_account_creation(self):
        account = personalAccount("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0, "Balance is not 0"
        assert account.pesel == "12345678901"
    
    def test_pesel_too_long(self):
        account = personalAccount("John", "Doe", '1234567890111')
        assert account.pesel == "Invalid"
    def test_pesel_too_short(self):
        account = personalAccount("John", "Doe", "123")
        assert account.pesel == "Invalid"
    
    def test_promo_code_valid(self):
        account = personalAccount("John", "Doe", "12345678901", "PROM_abc")
        assert account.balance == 50.0
    def test_promo_code_invalid_format(self):
        account = personalAccount("John", "Doe", "12345678901", "PurM_abc")
        assert account.balance == 0.0
    def test_promo_code_too_long(self):
        account = personalAccount("John", "Doe", "12345678901", "PROM_abcd")
        assert account.balance == 0.0
    def test_promo_code_too_short(self):
        account = personalAccount("John", "Doe", "12345678901", "PROM_ad")
        assert account.balance == 0.0

    def test_person_too_old(self):
        account = personalAccount("John", "Doe", "59115678901", "PROM_abc")
        assert account.balance == 0
    def test_person_age_ok(self):
        account = personalAccount("John", "Doe", "60115678901", "PROM_abc")
        assert account.balance == 50
    def test_person_age_born_after_2000(self):
        account = personalAccount("John", "Doe", "02215678901", "PROM_abc")
        assert account.balance == 50