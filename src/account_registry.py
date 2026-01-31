from src.personal_account import PersonalAccount
from typing import List

class AccountRegistry:
    def __init__(self):
        self.accounts: List[PersonalAccount] = []

    def clear(self):
        self.accounts.clear()


    def add_account(self, account):
        self.accounts.append(account)

    def get_account_by_pesel(self, pesel):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None

    def delete_account(self, pesel):
        account = self.get_account_by_pesel(pesel)
        if account is None:
            return False
        else: 
            self.accounts.remove(account)
        return True

    def get_all_accounts(self):
        return self.accounts

    def get_account_count(self):
        return len(self.accounts)