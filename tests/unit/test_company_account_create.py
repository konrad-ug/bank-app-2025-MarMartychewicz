from src.company_account import companyAccount

class TestCompanyAccount:
    def test_company_account_creation(self):
        account = companyAccount('CompanyName', '1234567890')
        assert account.company_name == "CompanyName"
        assert account.nip == '1234567890'
    def test_company_acc_incorrect_nip(self):
        account = companyAccount('CompanyName', '123')
        assert account.nip == 'Invalid'
        account2 = companyAccount('CompanyName2', '12345678901111111')
        assert account2.nip == 'Invalid'