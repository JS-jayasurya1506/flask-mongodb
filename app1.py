from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]


# CREATE
@app.route("/adddata", methods=["POST"])
def add_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    collection.insert_one(data)
    return jsonify({"message": "Data inserted successfully!"}), 201


# READ ALL
@app.route("/getdata", methods=["GET"])
def get_data():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)


# UPDATE by name
@app.route("/updatedata", methods=["PUT"])
def update_data():
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "Name is required"}), 400

    result = collection.update_one(
        {"name": data["name"]},
        {"$set": data}
    )

    if result.matched_count == 0:
        return jsonify({"message": "Data not found"}), 404

    return jsonify({"message": "Data updated successfully!"})


# DELETE by name
@app.route("/deletedata", methods=["DELETE"])
def delete_data():
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "Name is required"}), 400

    result = collection.delete_one({"name": data["name"]})

    if result.deleted_count == 0:
        return jsonify({"message": "Data not found"}), 404

    return jsonify({"message": "Data deleted successfully!"})


# READ ONE by numeric id field
@app.route("/getdata/<int:id>", methods=["GET"])
def get_data_by_id(id):
    data = collection.find_one({"id": id}, {"_id": 0})

    if data:
        return jsonify(data)

    return jsonify({"message": "Data not found"}), 404


# CONTACT FORM
@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"error": "All fields are required"}), 400

    contact_data = {
        "name": name,
        "email": email,
        "message": message
    }

    collection.insert_one(contact_data)

    return jsonify({
        "message": "Message received successfully!"
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
