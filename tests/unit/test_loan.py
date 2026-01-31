from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
import pytest

class TestAccount:

    @pytest.fixture(autouse=True)
    def account(self):
        account = PersonalAccount('John', 'Doe', '12345678901')
        return account

    @pytest.mark.parametrize('history, amount, expected_result, expected_balance', [
        ([100, 100, 100], 500, True, 800),
        ([-100,100,-100,100,1000], 700, True, 1700),
        ([100,100,-100,100,100], 500, False, 300),
        ([100,-100,100,100,100], 200, True, 500),
        ([200,1000,-100],1200,False,1100)
    ])
    def test_loan(self, account: PersonalAccount, history, amount, expected_result, expected_balance):
        for i in history:
            account.balance += i
        account.history = history
        result = account.submit_for_loan(amount)
        assert result == expected_result
        assert account.balance == expected_balance


    company_loan_tests = [
        ([4000,-1775,2000],4000,2000,True,6000),
        ([5000,-1775,-1000,3000],6000,2500,True,8500),
        ([3000,1000,-1775],3000,5000,False,3000),
        ([6000,-1000,4000],6000,4000,False,6000),
    ]
    ids = [
        'sufficient balance and ZUS payment',
        'sufficient balance and ZUS payment with multiple transactions',
        'insufficient balance',
        'no ZUS payment',
    ]
    @pytest.mark.parametrize("history, balance, amount, expected_result, expected_balance", company_loan_tests, ids=ids)
    def test_company_loan(self,history,balance,amount,expected_result, expected_balance):
        company_account = CompanyAccount('TestCorp', 1234567890)
        company_account.history = history
        company_account.balance = balance
        result = company_account.submit_for_loan(amount)
        assert result == expected_result
        assert company_account.balance == expected_balance

    #@pytest.fixture(autouse=True)
    #def prepare_database():
    #    #placeholder for database clearing logic
    #    yield
    #    #clear database after

    #@pytest.fixture
    #def company_account(self):
    #    account = PersonalAccount('John', 'Doe', '12345678901', iscompany=True) 
    #    return account
    
############################ old tests #######################################

    #def test_not_enough_transactions(self, account: PersonalAccount):
    #    account.history = [100, 100, 100, 300]
    #    account.balance = sum(account.history)
    #    result = account.submit_for_loan(500)
    #    assert not result
    #    assert account.balance == 600
    #
    #def test_past_three_transactions_werent_incoming(self):
    #    account = PersonalAccount('John', 'Doe', '12345678901')
    #    for i in range(4):
    #        account.incoming(50)
    #    account.outgoing(50)
#
    #    result = account.submit_for_loan(50)
    #    assert not result
    #    
    #    for i in range(2):
    #        account.incoming(50)
    #    assert account.submit_for_loan(50) == False
    #
    #def test_desired_loan_more_than_past_transactions(self):
    #    account = PersonalAccount('John', 'Doe', '12345678901')
    #    for i in range(6):
    #        account.incoming(50)
    #    assert account.submit_for_loan(500) == False
#
    #def loan_granted(self):
    #    account = PersonalAccount('John', 'Doe', '12345678901')
    #    for i in range(6):
    #        account.incoming(50)
    #    buf = account.balance
    #    assert account.submit_for_loan == True
    #    account.submit_for_loan(200)
    #    assert account.balance == buf + 200
    #