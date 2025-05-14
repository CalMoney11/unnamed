from flask import Flask, request, jsonify
from PIL import Image
import openai
import os
import base64
from io import BytesIO

app = Flask(__name__)
openai.api_key = os.getenv("API_Key_Calv")

@app.route("/api/critique", methods=["POST"])
def critique():
    print("\n[INFO] Incoming POST request to /api/critique")
    print("[DEBUG] Content-Type:", request.content_type)
    print("[DEBUG] Headers:", dict(request.headers))
    print("[DEBUG] Raw body (first 500 chars):")
    print(request.get_data()[:500])

    print("[DEBUG] request.files.keys():", list(request.files.keys()))
    print("[DEBUG] request.form.keys():", list(request.form.keys()))

    if "image" not in request.files:
        print("[ERROR] 'image' not in request.files")
        return jsonify({"error": "No valid image uploaded"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

