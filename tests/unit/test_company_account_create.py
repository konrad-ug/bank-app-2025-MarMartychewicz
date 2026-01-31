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

    def test_constructor_raises_when_nip_not_registered(self, mocker):
        mocker.patch(
            "src.company_account.CompanyAccount.nip_api_check",
            return_value=(False, False)
        )

        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Fake Company", "1234567890")

    def test_constructor_allows_vat_inactive_company(self, mocker):
        mocker.patch(
            "src.company_account.CompanyAccount.nip_api_check",
            return_value=(True, False)
        )

        acc = CompanyAccount("Inactive VAT Co", "1234567890")
        assert acc.company_name == "Inactive VAT Co"

    def test_constructor_allows_vat_active_company(self, mocker):
        mocker.patch(
            "src.company_account.CompanyAccount.nip_api_check",
            return_value=(True, True)
        )

        acc = CompanyAccount("Active VAT Co", "1234567890")
        assert acc.company_name == "Active VAT Co"

    def test_short_nip_does_not_call_api(self, mocker):
        mock = mocker.patch(
            "src.company_account.CompanyAccount.nip_api_check"
        )

        CompanyAccount("Short NIP Co", "123")

        mock.assert_not_called()



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