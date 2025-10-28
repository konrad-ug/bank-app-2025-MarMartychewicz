from src.account import Account
from src.personal_account import PersonalAccount

class TestTransaction:
    def test_incoming_transaction_is_NaN(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.incoming('NaN')
        assert account.balance == 0.0
    def test_incoming_transaction(self):
        account = PersonalAccount("John", "Doe", "12345678901")
        account.incoming(60.0)
        assert account.balance == 60.0
    def test_outgoing_transaction(self):
        account = PersonalAccount("John", "Doe", "12345678901", "PROM_abc")
        assert account.balance == 50.0
        account.outgoing(20.0)
        assert account.balance == 30.0
    def test_outgoing_transaction_insufficient_funds(self):
        account = PersonalAccount("John", "Doe", "12345678901", "PROM_abc")
        assert account.balance == 50.0
        assert account.outgoing(60.0) == 'error: Not enough funds to complete transaction'
        account.outgoing(60.0)
        assert account.balance == 50.0