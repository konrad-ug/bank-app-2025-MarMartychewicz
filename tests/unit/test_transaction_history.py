from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestPersonalTransactionHistory:
    account = PersonalAccount("John", "Doe", "12345678901")
    assert account.history == []
    account.incoming(460)
    assert account.history == [460]
    account.outgoing(60)
    assert account.history == [460, -60]
    account.express(95)
    assert account.history == [460, -60, -95, -account.express_outgoing_fee]
    account.outgoing(600)
    assert account.history == [460, -60, -95, -account.express_outgoing_fee]


class TestCompanyTransactionHistory:
    account = CompanyAccount('CompanyName', '1234567890')
    assert account.history == []
    account.incoming(460)
    assert account.history == [460]
    account.outgoing(60)
    assert account.history == [460, -60]
    account.express(95)
    assert account.history == [460, -60, -95, -account.express_outgoing_fee]
    account.outgoing(600)
    assert account.history == [460, -60, -95, -account.express_outgoing_fee]