from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount
from src.repositories.mongo_accounts_repository import MongoAccountsRepository

def get_repository():
    return MongoAccountsRepository()

app = Flask(__name__)
registry = AccountRegistry()
repository = get_repository()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    if registry.get_account_by_pesel(data["pesel"]):
        return jsonify({"error": "There already is an account with this pesel"}), 409

    account = PersonalAccount(data["name"], data["surname"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.get_all_accounts()
    if accounts == []:
        return jsonify({"error": "Accounts not found"}), 404
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel": acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get account count request received")
    count = registry.get_account_count()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    acc = registry.get_account_by_pesel(pesel)
    if acc is None:
        return jsonify({"error": "Account not found"}), 404
    acc_data = {"name": acc.first_name, "surname": acc.last_name, "pesel": acc.pesel, "balance": acc.balance}
    return jsonify(acc_data), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    acc = registry.get_account_by_pesel(pesel)
    if acc is None:
        return jsonify({"error": "Account not found"}), 404

    if "name" in data:
        acc.first_name = data["name"]
    if "surname" in data:
        acc.last_name = data["surname"]

    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    success = registry.delete_account(pesel)
    if not success:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({"message": "Account deleted"}), 200

@app.route('/api/accounts/<pesel>/transfer', methods=['PATCH'])
def transfer(pesel):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    acc = registry.get_account_by_pesel(pesel)
    if acc is None:
        return jsonify({"error": "Account not found"}), 404

    amount = data['amount']
    if not isinstance(amount, int or float):
        return jsonify({'error': 'The provided amount is not a number'}), 422

    match data['type']:
        case 'incoming':
            if acc.incoming(amount):
                return jsonify({'message': 'The order has been accepted'}), 200

        case 'outgoing':
            if acc.balance > amount:
                acc.outgoing(amount)
                return jsonify({'message': 'The order has been accepted'}), 200
            elif acc.outgoing(amount) == 'error: Not enough funds to complete transaction':
                return jsonify({'error': 'Not enough funds to complete the transaction'}), 422

        case 'express':
            if acc.balance > acc.express_cost:
                acc.express(amount)
                return jsonify({'message': 'The order has been accepted'}), 200
            elif acc.express(amount) == 'error: Not enough funds to complete transaction':
                return jsonify({'error': 'Not enough funds to complete the transaction'}), 422

        case 'debug':
            acc.balance = amount
            return jsonify({'message': 'The order has been accepted'}), 200

        case _:
            pass

@app.route("/api/accounts/save", methods=["POST"])
def save_accounts():
    accounts = registry.get_all_accounts()
    repository.save_all(accounts)
    return jsonify({"message": "Accounts saved"}), 200

@app.route("/api/accounts/load", methods=["POST"])
def load_accounts():
    # Clear current registry
    registry.clear()

    # Load from DB
    accounts = repository.load_all()
    for acc in accounts:
        registry.add_account(acc)

    return jsonify({"message": "Accounts loaded"}), 200
