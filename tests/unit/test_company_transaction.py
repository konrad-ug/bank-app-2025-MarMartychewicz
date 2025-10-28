from src.company_account import CompanyAccount

class TestCompanyTransaction:
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