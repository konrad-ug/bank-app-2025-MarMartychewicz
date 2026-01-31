from src.account import Account
from src.personal_account import PersonalAccount
import pytest

class TestTransaction:
    @pytest.fixture(autouse=True)
    def account(self):
        account = PersonalAccount('John', 'Doe', '12345678901')
        return account
    
    @pytest.mark.parametrize('balance, transaction_type, amount, expected_result, expected_balance', [
        (0, 'incoming', 'NaN', 'error: incoming sum is not a number', 0),
        (0,'incoming',60,True,60),
        (50,'outgoing',20,True,30),
        (50,'outgoing',60,'error: Not enough funds to complete transaction',50)
    ])
    def test_transaction(self, account: PersonalAccount, balance, transaction_type, amount, expected_result, expected_balance):
        account.balance = balance
        if transaction_type == 'incoming':
            assert account.incoming(amount) == expected_result
            assert account.balance == expected_balance
        elif transaction_type == 'outgoing':
            assert account.outgoing(amount) == expected_result
            assert account.balance == expected_balance

#class TestTransaction:
#    def test_incoming_transaction_is_NaN(self):
#        account = PersonalAccount("John", "Doe", "12345678901")
#        account.incoming('NaN')
#        assert account.balance == 0.0
#    def test_incoming_transaction(self):
#        account = PersonalAccount("John", "Doe", "12345678901")
#        account.incoming(60.0)
#        assert account.balance == 60.0
#    def test_outgoing_transaction(self):
#        account = PersonalAccount("John", "Doe", "12345678901")
#        account.balance = 50
#        assert account.balance == 50.0
#        account.outgoing(20.0)
#        assert account.balance == 30.0
#    def test_outgoing_transaction_insufficient_funds(self):
#        account = PersonalAccount("John", "Doe", "12345678901")
#        account.balance = 50
#        assert account.balance == 50.0
#        assert account.outgoing(60.0) == 'error: Not enough funds to complete transaction'
#        account.outgoing(60.0)
#        assert account.balance == 50.0