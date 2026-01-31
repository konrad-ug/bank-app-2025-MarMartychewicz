from unittest.mock import MagicMock
from app.api import app, registry


def test_save_endpoint_calls_repository(monkeypatch):
    mock_repo = MagicMock()

    # Replace real repository with mock
    monkeypatch.setattr("app.api.repository", mock_repo)

    client = app.test_client()

    response = client.post("/api/accounts/save")

    assert response.status_code == 200
    mock_repo.save_all.assert_called_once()


def test_load_endpoint_clears_registry_and_loads(monkeypatch):
    mock_repo = MagicMock()

    fake_account = MagicMock()
    fake_account.pesel = "123"

    mock_repo.load_all.return_value = [fake_account]

    monkeypatch.setattr("app.api.repository", mock_repo)

    # Put something into registry to ensure it is cleared
    registry.accounts.clear()
    registry.accounts.append(MagicMock())

    client = app.test_client()
    response = client.post("/api/accounts/load")

    assert response.status_code == 200
    assert len(registry.accounts) == 1
    assert registry.accounts[0] == fake_account
