from unittest.mock import MagicMock
from app.api import app, registry


def test_save_accounts_calls_repository(monkeypatch):

    mock_repository = MagicMock()

    # Replace real repository with mock
    monkeypatch.setattr("app.api.repository", mock_repository)

    client = app.test_client()

    response = client.post("/api/accounts/save")

    assert response.status_code == 200
    mock_repository.save_all.assert_called_once()


def test_load_accounts_clears_registry_and_loads_from_repository(monkeypatch):

    mock_repository = MagicMock()

    fake_account = MagicMock()
    fake_account.pesel = "99999999999"

    mock_repository.load_all.return_value = [fake_account]

    monkeypatch.setattr("app.api.repository", mock_repository)

    # Put something in registry to ensure it is cleared
    registry.accounts.clear()
    registry.accounts.append(MagicMock())

    client = app.test_client()
    response = client.post("/api/accounts/load")

    assert response.status_code == 200
    assert len(registry.accounts) == 1
    assert registry.accounts[0] is fake_account
