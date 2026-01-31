from src.company_account import CompanyAccount
import pytest

class TestCompanyTransaction:
    @pytest.fixture(autouse=True)
    def account(self):
        account = CompanyAccount('CompanyName', '1234567890')
        return account
    
    @pytest.mark.parametrize('balance, transaction_type, amount, expected_result, expected_balance', [
        (0,'incoming',250,True,250),
        (500,'outgoing',50,True,450),
        (10,'outgoing',50,'error: Not enough funds to complete transaction',10),
        (10,'outgoing','w','error: outgoing sum is not a number',10)
    ])
    def test_company_transaction(self, account: CompanyAccount, balance, transaction_type, amount, expected_result, expected_balance):
        account.balance = balance
        
        if transaction_type == 'incoming':
            assert account.incoming(amount) == expected_result
        elif transaction_type == 'outgoing':
            assert account.outgoing(amount) == expected_result
        
        assert account.balance == expected_balance

#class TestCompanyTransaction:
#    def test_company_acc_incoming(self):
#        account = CompanyAccount('CompanyName', '1234567890')
#        account.incoming(250.0)
#        assert account.balance == 250
#    def test_company_acc_outgoing(self):
#        account = CompanyAccount('CompanyName', '1234567890')
#        account.balance = 500.0
#        account.outgoing(50)
#        assert account.balance == 450
#    def test_company_acc_outgoing_insufficient_funds(self):
#        account = CompanyAccount('CompanyName', '1234567890')
#        account.balance = 10.0
#        assert account.outgoing(50) == 'error: Not enough funds to complete transaction'
#        account.outgoing(50)
#        assert account.balance == 10
#    def test_company_acc_outgoing_NaN(self):
#        account = CompanyAccount('CompanyName', '1234567890')
#        account.balance = 10.0
#        assert account.outgoing('w') == 'error: outgoing sum is not a number'
#        account.outgoing('w')
#        assert account.balance == 10