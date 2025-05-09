from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
mongo_uri = os.environ.get('MONGO_URI')
client = MongoClient(mongo_uri)
db = client['bls']
collection = db['loan_requests']

@app.route('/loan/apply', methods=['POST'])
def apply_loan():
    data = request.json
    data['status'] = 'submitted'
    collection.insert_one(data)
    return jsonify({"message": "Loan application submitted", "data": data}), 201

@app.route('/loan/status/<email>', methods=['GET'])
def loan_status(email):
    loan = collection.find_one({"email": email})
    if not loan:
        return jsonify({"error": "Not found"}), 404
    loan['_id'] = str(loan['_id'])
    return jsonify(loan), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
