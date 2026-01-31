from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount
import pytest

class TestAccountRegistry:
    @pytest.fixture
    def registry(self):
        return AccountRegistry()
    
    @pytest.fixture
    def account1(self):
        account1 = PersonalAccount('John','Doe','89092909876')
        return account1
    
    @pytest.fixture
    def account2(self):
        account2 = PersonalAccount('Jane','Deer','89092909877')
        return account2
    
    def test_add_and_get_account(self, registry: AccountRegistry, account1: PersonalAccount):
        registry.add_account(account1)
        assert registry.get_account_by_pesel('89092909876') == account1
    
    def test_get_account_not_found(self, registry: AccountRegistry):
        assert registry.get_account_by_pesel('00000000000') is None
    
    def test_get_all_accounts(self, registry: AccountRegistry, account1: PersonalAccount, account2: PersonalAccount):
        registry.add_account(account1)
        registry.add_account(account2)
        assert registry.get_all_accounts() == [account1, account2]

    def test_get_account_count(self, registry: AccountRegistry, account1: PersonalAccount, account2: PersonalAccount):
        registry.add_account(account1)
        registry.add_account(account2)
        assert registry.get_account_count() == 2
    
    def test_remove_account(self, registry: AccountRegistry, account1: PersonalAccount, account2: PersonalAccount):
        registry.add_account(account1)
        registry.add_account(account2)
        assert registry.delete_account(account1.pesel) == True
        assert registry.get_all_accounts() == [account2]

        assert registry.delete_account(11111111101) == False