from datetime import datetime
import os

from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient(
    os.environ.get(
        "MONGODB_URI",
        "mongodb://localhost:27017/",
    )
)
collection = client.flask_db.data


@app.route("/")
def index():
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"


@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        document = request.get_json()
        collection.insert_one(document)
        return jsonify({"status": "Data inserted"}), 201

    documents = list(collection.find({}, {"_id": 0}))
    return jsonify(documents), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)