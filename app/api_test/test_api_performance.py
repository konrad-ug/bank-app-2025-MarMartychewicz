import requests, pytest, random

BASE_URL = "http://127.0.0.1:5000"
time_limit = 0.5

def test_create_delete_account_perf():
    for i in range(100):
        pesel = str(random.randrange(10000000000, 99999999999))

        response = requests.post(f'{BASE_URL}/api/accounts', json={'name': 'Jonathan', 'surname': 'Deer', 'pesel': pesel}, timeout=time_limit)
        assert response.status_code == 201

        del_request = requests.delete(f'{BASE_URL}/api/accounts/{pesel}', timeout=time_limit)
        assert del_request.status_code == 200

def test_create_acc_incoming_transf_perf():
    for i in range(100):
        pesel = str(random.randrange(10000000000, 99999999999))
        amount = random.randrange(1, 10000)

        response = requests.post(f'{BASE_URL}/api/accounts', json={'name': 'Jonathan', 'surname': 'Deer', 'pesel': pesel}, timeout=time_limit)
        assert response.status_code == 201

        response = requests.patch(f'{BASE_URL}/api/accounts/{pesel}/transfer', json={'type': 'incoming', 'amount': amount}, timeout=time_limit)
        assert response.status_code == 200

        response = requests.get(f'{BASE_URL}/api/accounts/{pesel}')
        data = response.json()
        assert data['balance'] == amount

def test_create_delete_account_perf_extreme(): # Przy usuwaniu po stworzeniu wszytskich kont, funkcja szukająca konto do usunięcia ma ""więcej pracy""
    pesel_list = []
    for i in range(1000):
        while True:
            pesel = str(random.randrange(10000000000, 99999999999))
            if pesel not in pesel_list:
                break

        response = requests.post(f'{BASE_URL}/api/accounts', json={'name': 'Jonathan', 'surname': 'Deer', 'pesel': pesel}, timeout=time_limit)
        assert response.status_code == 201

    for pesel in pesel_list:
        del_request = requests.delete(f'{BASE_URL}/api/accounts/{pesel}', timeout=time_limit)
        assert del_request.status_code == 200
    