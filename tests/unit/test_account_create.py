from src.personal_account import PersonalAccount
import pytest

class TestAccount:
    account_creation_tests = [
        ('John', 'Doe', '12345678901', '12345678901', None, 0),
        ('John', 'Doe', '1234567890111', 'Invalid', None, 0),
        ('John', 'Doe', '123', 'Invalid', None, 0),

        ('John', 'Doe', '12345678901', '12345678901', 'PROM_abc', 50),
        ('John', 'Doe', '12345678901', '12345678901', 'PurM_abc', 0),
        ('John', 'Doe', '12345678901', '12345678901', 'PROM_abcd', 0),
        ('John', 'Doe', '12345678901', '12345678901', 'PROM_ad', 0),

        ('John', 'Doe', '59115678901', '59115678901', 'PROM_abc', 0),
        ('John', 'Doe', '60115678901', '60115678901', 'PROM_abc', 50),
        ('John', 'Doe', '02215678901', '02215678901', 'PROM_abc', 50),
    ]
    ids = [
        'Account created correctly',
        'Pesel too long',
        'Pesel too short',

        'Valid promo code',
        'Invalid promo code format',
        'Promo code too long',
        'Promo code too short',

        'Person too old for promo',
        'Person qualifies for promo',
        'Person qualifies for promo - born after 2000',
    ]
    @pytest.mark.parametrize('name, surname, pesel, expected_pesel, promo, expected_balance', account_creation_tests, ids=ids)
    def test_account_creation(self, name, surname, pesel, expected_pesel, promo, expected_balance):
        account = PersonalAccount(name,surname,pesel,promo)
        assert account.first_name == name
        assert account.last_name == surname
        assert account.pesel == expected_pesel
        assert account.balance == expected_balance

    #def test_account_creation(self):
    #    account = PersonalAccount("John", "Doe", "12345678901")
    #    assert account.first_name == "John"
    #    assert account.last_name == "Doe"
    #    assert account.balance == 0.0, "Balance is not 0"
    #    assert account.pesel == "12345678901"
    #
    #def test_pesel_too_long(self):
    #    account = PersonalAccount("John", "Doe", '1234567890111')
    #    assert account.pesel == "Invalid"
    #def test_pesel_too_short(self):
    #    account = PersonalAccount("John", "Doe", "123")
    #    assert account.pesel == "Invalid"
#
    #def test_promo_code_valid(self):
    #    account = PersonalAccount("John", "Doe", "12345678901", "PROM_abc")
    #    assert account.balance == 50.0
    #def test_promo_code_invalid_format(self):
    #    account = PersonalAccount("John", "Doe", "12345678901", "PurM_abc")
    #    assert account.balance == 0.0
    #def test_promo_code_too_long(self):
    #    account = PersonalAccount("John", "Doe", "12345678901", "PROM_abcd")
    #    assert account.balance == 0.0
    #def test_promo_code_too_short(self):
    #    account = PersonalAccount("John", "Doe", "12345678901", "PROM_ad")
    #    assert account.balance == 0.0
#
    #def test_person_too_old(self):
    #    account = PersonalAccount("John", "Doe", "59115678901", "PROM_abc")
    #    assert account.balance == 0
    #def test_person_age_ok(self):
    #    account = PersonalAccount("John", "Doe", "60115678901", "PROM_abc")
    #    assert account.balance == 50
    #def test_person_age_born_after_2000(self):
    #    account = PersonalAccount("John", "Doe", "02215678901", "PROM_abc")
    #    assert account.balance == 50