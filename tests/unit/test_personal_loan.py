from src.personal_account import PersonalAccount
import pytest

class TestApplyForLoan:

    @pytest.fixture(autouse=True)
    def account(self):
        account = PersonalAccount('John', 'Doe', '12345678901')
        return account

    @pytest.mark.parametrize('history, amount, expected_result, expected_balance', [
        ([100, 100, 100], 500, False, 300),
        ([-100,100,-100,100,1000], 700, False, 1000),
        ([100,-100,100,100,100], 500, False, 300),
        ([100,-100,100,100,100], 200, True, 500)
    ])
    def test_loan(self, account: PersonalAccount, history, amount, expected_result, expected_balance):
        for i in history:
            account.balance += i
        account.history = history
        result = account.submit_for_loan(amount)
        assert result == expected_result
        assert account.balance == expected_balance

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