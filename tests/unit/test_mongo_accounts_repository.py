from unittest.mock import MagicMock, patch
from src.repositories.mongo_accounts_repository import MongoAccountsRepository


def test_save_all_clears_collection_and_inserts_documents():
    # Arrange
    mock_collection = MagicMock()
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection
    mock_client = MagicMock()
    mock_client.__getitem__.return_value = mock_db

    with patch("src.repositories.mongo_accounts_repository.MongoClient", return_value=mock_client):
        repo = MongoAccountsRepository()

        account1 = MagicMock(
            first_name="john",
            last_name="doe",
            pesel="12345678901",
            balance=100,
            history=[100],
        )
        account2 = MagicMock(
            first_name="jane",
            last_name="doe",
            pesel="98765432101",
            balance=200,
            history=[200],
        )

        # Act
        repo.save_all([account1, account2])

        # Assert
        mock_collection.delete_many.assert_called_once_with({})
        mock_collection.insert_many.assert_called_once()

        inserted_docs = mock_collection.insert_many.call_args[0][0]
        assert len(inserted_docs) == 2
        assert inserted_docs[0]["first_name"] == "john"
        assert inserted_docs[1]["pesel"] == "98765432101"

def test_save_all_with_empty_accounts_does_not_insert():
    mock_collection = MagicMock()
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection
    mock_client = MagicMock()
    mock_client.__getitem__.return_value = mock_db

    with patch("src.repositories.mongo_accounts_repository.MongoClient", return_value=mock_client):
        repo = MongoAccountsRepository()

        repo.save_all([])

        mock_collection.delete_many.assert_called_once_with({})
        mock_collection.insert_many.assert_not_called()

def test_load_all_returns_personal_accounts():
    mock_collection = MagicMock()
    mock_collection.find.return_value = [
        {
            "first_name": "john",
            "last_name": "doe",
            "pesel": "12345678901",
            "balance": 500,
            "history": [500],
        },
        {
            "first_name": "jane",
            "last_name": "smith",
            "pesel": "98765432101",
            "balance": 300,
            "history": [300],
        },
    ]

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_collection
    mock_client = MagicMock()
    mock_client.__getitem__.return_value = mock_db

    with patch("src.repositories.mongo_accounts_repository.MongoClient", return_value=mock_client):
        repo = MongoAccountsRepository()

        accounts = repo.load_all()

        assert len(accounts) == 2
        assert accounts[0].first_name == "john"
        assert accounts[0].balance == 500
        assert accounts[1].pesel == "98765432101"
        assert accounts[1].history == [300]
