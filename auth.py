from flask import Flask, request, jsonify
from pymongo import MongoClient

auth = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    password = data["password"]

    existing_user = collection.find_one({"email": email})

    if existing_user:
        return jsonify({"message": "User already exists!"}), 400

    collection.insert_one({
        "name": name,
        "email": email,
        "password": password
    })

    return jsonify({"message": "User registered successfully!"}), 201


if __name__ == "__main__":
    auth.run(debug=True)