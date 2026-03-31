from flask import Flask, request, jsonify, send_from_directory
import os
import random
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

latest_data = {
    "people_count": 0,
    "time": "",
    "image": ""
}

API_KEY = "wenotice123"


@app.route("/")
def home():
    return "WeNotice AI Running 🚀"


@app.route("/detect-headcount", methods=["POST"])
def detect():

    key = request.headers.get("x-api-key")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 403

    image_bytes = request.data

    filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "wb") as f:
        f.write(image_bytes)

    # 🎲 Simulated AI (random number)
    count = random.randint(1, 5)

    time_now = datetime.now().strftime("%H:%M:%S")

    latest_data["people_count"] = count
    latest_data["time"] = time_now
    latest_data["image"] = filename

    return jsonify(latest_data)


@app.route("/latest")
def latest():
    return jsonify(latest_data)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)