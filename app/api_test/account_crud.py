import requests, pytest

BASE_URL = "http://127.0.0.1:5000"

class TestApi:
    
    @pytest.fixture
    def account1(self):
        account1 = {
            'name': 'John',
            'surname': 'Doe',
            'pesel': '12345678901'
        }
        return account1
    
    @pytest.fixture
    def account2(self):
        account2 = {
            'name': 'Jane',
            'surname': 'Deer',
            'pesel': '32165498707'
        }
        #response = requests.post(f'{BASE_URL}/api/accounts', json={
        #    'name': 'Jane',
        #    'surname': 'Deer',
        #    'pesel': '32165498707'
        #})
        return account2

    def test_create(self, account1, account2):
        create_account = requests.post(f'{BASE_URL}/api/accounts', json=account1)
        create_account2 = requests.post(f'{BASE_URL}/api/accounts', json=account2)
        assert create_account.status_code == 201
        assert create_account.json()['message'] == 'Account created'
        assert create_account2.status_code == 201
        assert create_account2.json()['message'] == 'Account created'

        #second account on the same pesel:
        create_account3 = requests.post(f'{BASE_URL}/api/accounts', json=account1)
        assert create_account3.status_code == 409
        assert create_account3.json()['error'] == 'There already is an account with this pesel'
    
    def test_get_all(self, account1, account2):
        get_acc = requests.get(f'{BASE_URL}/api/accounts')

        data = get_acc.json()
        assert isinstance(data,list)
        assert get_acc.status_code == 200
        assert data[0] == { 'balance': 0, 'name': 'John', 'surname': 'Doe', 'pesel': '12345678901' }
        assert data[1] == { 'balance': 0, 'name': 'Jane', 'surname': 'Deer', 'pesel': '32165498707' }

    def test_get_count(self):
        get_count = requests.get(f'{BASE_URL}/api/accounts/count')

        get_count = requests.get(f'{BASE_URL}/api/accounts/count')
        data = get_count.json()
        assert get_count.status_code == 200
        assert data["count"] == 2
    
    @pytest.mark.parametrize('account1, account2, pesel, expected_response, expected_status_code', [
        (account1, account2, '12345678901', { 'balance': 0, 'name': 'John', 'surname': 'Doe', 'pesel': '12345678901' }, 200),
        (account1, account2, '11111111101', {"error": "Account not found"}, 404)
    ])
    def test_get_by_pesel(self, account1, account2, pesel, expected_response, expected_status_code):
        get_acc = requests.get(f'{BASE_URL}/api/accounts/{pesel}')

        assert get_acc.status_code == expected_status_code
        assert get_acc.json() == expected_response

    account_update_tests = [
        ('12345678901', {}, 400, {"error": "No data provided"}),
        ('11111111101', {'name': 'Jameson', 'surname': 'Canine'}, 404, {"error": "Account not found"}),
        ('12345678901', {'name': 'Jameson', 'surname': 'Canine'}, 200, {"message": "Account updated"}),
    ]
    ids = [
        'No data provided',
        'No account with provided pesel',
        'Successful update'
    ]
    @pytest.mark.parametrize('pesel, data, expected_status_code, expected_response', account_update_tests, ids=ids)
    def test_update_acc(self, pesel, data, expected_status_code, expected_response):

        get_acc = requests.get(f'{BASE_URL}/api/accounts/{pesel}')

        upd_acc = requests.patch(f'{BASE_URL}/api/accounts/{pesel}', json=data)
        assert upd_acc.status_code == expected_status_code
        assert upd_acc.json() == expected_response


    transfer_tests = [
        ('12345678901', 5, 'incoming', 5, 10),
        ('12345678901', 5, 'incoming', 'w', 5),

        ('12345678901', 100, 'outgoing', 50, 50),
        ('12345678901', 100, 'outgoing', 150, 100),
        ('12345678901', 100, 'outgoing', 'w', 100),
        ('12345672301', 100, 'outgoing', 50, 100),

        ('12345672301', 100, 'express', 50, 49),
        ('12345672301', 100, 'express', 150, -51),
        ('12345672301', 0, 'express', 50, 0),
    ]
    ids=[
        'Incoming transaction',
        'Incoming transaction amount NaN',

        'Outgoing transaction',
        'Not enough funds to complete transaction',
        'Outgoing NaN',
        'Wrong pesel',

        'Express transaction',
        'Express transaction (amount higher than balance)',
        'Express fee higher than balance'
    ]
    @pytest.mark.parametrize('pesel, balance, transfer_type, amount, expected_balance', transfer_tests, ids=ids)
    def test_transfers(self, pesel, balance, transfer_type, amount, expected_balance):
        #Setup balance for testing
        debug = requests.patch(f'{BASE_URL}/api/accounts/{pesel}/transfer', json={'amount': balance, 'type': 'debug'})
        transfer = requests.patch(f'{BASE_URL}/api/accounts/{pesel}/transfer', json={'amount': amount, 'type': transfer_type})

        #Unknown pesels
        get_acc = requests.get(f'{BASE_URL}/api/accounts/{pesel}')
        if get_acc.status_code == 404:
            assert debug.status_code == 404
            assert debug.json() == {"error": "Account not found"}

        elif not isinstance(amount, int or float):
            assert transfer.status_code == 422
            assert transfer.json() == {'error': 'The provided amount is not a number'}
        else:
            match transfer_type:
                case 'incoming':
                    assert transfer.status_code == 200
                    assert transfer.json() == {'message': 'The order has been accepted'}
                case 'outgoing':
                    if amount > balance:
                        assert transfer.status_code == 422
                        assert transfer.json() == {'error': 'Not enough funds to complete the transaction'}
                    else:
                        assert transfer.status_code == 200
                        assert transfer.json() == {'message': 'The order has been accepted'}
                case 'express':
                    if balance < 1: # express fee = 1
                        assert transfer.status_code == 422
                        assert transfer.json() == {'error': 'Not enough funds to complete the transaction'}
                    else:
                        assert transfer.status_code == 200
                        assert transfer.json() == {'message': 'The order has been accepted'}
                case _:
                    assert transfer.status_code == 400 # - bad request
                    assert transfer.json() == {'error': 'Unknown transaction type'}

        status = requests.get(f'{BASE_URL}/api/accounts/{pesel}')
        if status.status_code != 404:
            data = status.json()
            assert data['balance'] == expected_balance


    def test_delete_account(self, account2):
        pesel = account2['pesel']
        
        get_count = requests.get(f'{BASE_URL}/api/accounts/count')
        data = get_count.json()
        assert data["count"] == 2

        del_acc = requests.delete(f'{BASE_URL}/api/accounts/{pesel}')
        assert del_acc.status_code == 200
        assert del_acc.json() == {"message": "Account deleted"}

        get_count = requests.get(f'{BASE_URL}/api/accounts/count')
        data = get_count.json()
        assert data["count"] == 1