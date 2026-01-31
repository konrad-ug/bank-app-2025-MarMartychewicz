from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
import pytest

class TestPersonalExpressTransaction:

    @pytest.fixture(autouse=True)
    def account(self):
        account = PersonalAccount('John', 'Doe', 12345678901)
        return account
    
    @pytest.mark.parametrize('balance, express_amount, express_result, expected_balance', [
        (10,20,True,-11),
        (0,20,'error: Not enough funds to complete transaction',0),
        (10,'w','error: outgoing sum is not a number',10)
    ])
    def test_express_transaction(self, account: PersonalAccount, balance, express_amount, express_result, expected_balance):
        account.balance = balance
        assert account.express(express_amount) == express_result
        account.express(express_amount)
        assert account.balance == expected_balance

class TestCompanyExpresTransaction:
    @pytest.fixture(autouse=True)
    def account(self):
        account = CompanyAccount('testCom', 1234567890)
        return account
    
    @pytest.mark.parametrize('balance, express_amount, express_result, expected_balance', [
        (10,20,True,-15),
        (4,20,'error: Not enough funds to complete transaction',4),
        (10,'w','error: outgoing sum is not a number',10)
    ])
    def test_express_transaction(self, account: CompanyAccount, balance, express_amount, express_result, expected_balance):
        account.balance = balance
        assert account.express(express_amount) == express_result
        account.express(express_amount)
        assert account.balance == expected_balance


#class TestPersonalExpressTransaction:
#    def test_express_transaction(self):
#        account = PersonalAccount('John', 'Doe', 12345678901)
#        account.balance = 10
#        account.express(20)
#        assert account.balance == -11
#    
#    def test_express_not_enough(self):
#        account = PersonalAccount('John', 'Doe', 12345678901)
#        account.balance = 0
#        assert account.express(20) == 'error: Not enough funds to complete transaction'
#        account.express(20)
#        assert account.balance == 0
#    
#    def test_express_invalid_value(self):
#        account = PersonalAccount('John', 'Doe', 12345678901)
#        account.balance = 10
#        assert account.express('w') == 'error: outgoing sum is not a number'
#        account.express('w')
#        assert account.balance == 10
#
#class TestCompanyExpresTransaction:
#    def test_express_transaction(self):
#        account = CompanyAccount('testCom', 1234567890)
#        account.balance = 10
#        account.express(20)
#        assert account.balance == -15
#
#    def test_express_not_enough(self):
#        account = CompanyAccount('testCom', 1234567890)
#        account.balance = 4
#        assert account.express(20) == 'error: Not enough funds to complete transaction'
#        account.express(20)
#        assert account.balance == 4
#
#    def test_express_invalid_value(self):
#        account = CompanyAccount('testCom', 1234567890)
#        account.balance = 10
#        assert account.express('w') == 'error: outgoing sum is not a number'
#        account.express('w')
#        assert account.balance == 10