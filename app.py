from flask import Flask, request, jsonify, send_from_directory
from ultralytics import YOLO
import cv2
import os
from datetime import datetime

app = Flask(__name__)

# Load AI model
model = YOLO("yolov8n.pt")

# Create uploads folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Simple security key
API_KEY = "wenotice123"


@app.route("/")
def home():
    return "WeNotice AI Running 🚀"


@app.route("/detect-headcount", methods=["POST"])
def detect():

    # Check API key
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 403

    # Get image from ESP32
    image_bytes = request.data

    if not image_bytes:
        return jsonify({"error": "No image received"}), 400

    # Save image
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "wb") as f:
        f.write(image_bytes)

    # Read image
    image = cv2.imread(filepath)

    # Run AI
    results = model(image)

    count = 0

    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:  # person class
                count += 1

    return jsonify({
        "people_count": count,
        "image": filename
    })


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)