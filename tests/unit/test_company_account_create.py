from src.company_account import CompanyAccount
import pytest

class TestCompanyAccount:

    @pytest.mark.parametrize('company_name, nip, expected_nip', [
        ('TestCompany', 1234567890, 1234567890),
        ('TestCompany', 123, 'Invalid'),
        ('TestCompany', 12345678901111111, 'Invalid')
    ])
    def test_company_account_creation(self, company_name, nip, expected_nip):
        account = CompanyAccount(company_name, nip)
        assert account.company_name == company_name
        assert account.nip == expected_nip

#class TestCompanyAccount:
#    def test_company_account_creation(self):
#        account = CompanyAccount('CompanyName', '1234567890')
#        assert account.company_name == "CompanyName"
#        assert account.nip == '1234567890'
#    def test_company_acc_incorrect_nip(self):
#        account = CompanyAccount('CompanyName', '123')
#        assert account.nip == 'Invalid'
#        account2 = CompanyAccount('CompanyName2', '12345678901111111')
#        assert account2.nip == 'Invalid'