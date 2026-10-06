from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]


@app.route("/adddata", methods=["POST"])
def add_data():
    data = request.get_json()
    collection.insert_one(data)
    return jsonify({"message": "Data inserted successfully!"})


@app.route("/getdata", methods=["GET"])
def get_data():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)


@app.route("/updatedata", methods=["PUT"])
def update_data():
    data = request.get_json()
    query = {"name": data["name"]}
    new_values = {"$set": data}
    collection.update_one(query, new_values)
    return jsonify({"message": "Data updated successfully!"})


@app.route("/deletedata", methods=["DELETE"])
def delete_data():
    data = request.get_json()
    query = {"name": data["name"]}
    collection.delete_one(query)
    return jsonify({"message": "Data deleted successfully!"})


@app.route("/getdata/<int:id>", methods=["GET"])
def get_data_by_id(id):
    data = collection.find_one({"id": id}, {"_id": 0})

    if data:
        return jsonify(data)
    else:
        return jsonify({"message": "Data not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)