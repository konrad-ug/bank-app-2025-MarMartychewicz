from pymongo import MongoClient
from src.personal_account import PersonalAccount


class MongoAccountsRepository:
    def __init__(
        self,
        uri: str = "mongodb://localhost:27017",
        db_name: str = "bank",
        collection_name: str = "accounts"
    ):
        #initialize MongoDB
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_all(self, accounts):
        #Saves all accounts to MongoDB.

        # Clear collection first
        self.collection.delete_many({})

        documents = []

        for acc in accounts:
            documents.append({
                "first_name": acc.first_name,
                "last_name": acc.last_name,
                "pesel": acc.pesel,
                "balance": acc.balance,
                "history": acc.history
            })

        if documents:
            self.collection.insert_many(documents)
    
    def load_all(self):
        accounts = []

        for doc in self.collection.find({}):
            account = PersonalAccount(
                doc["first_name"],
                doc["last_name"],
                doc["pesel"]
            )
            account.balance = doc["balance"]
            account.history = doc["history"]

            accounts.append(account)

        return accounts