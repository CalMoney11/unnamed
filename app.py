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

    print("[DEBUG] request.files keys:", list(request.files.keys()))
    print("[DEBUG] request.form keys:", list(request.form.keys()))
    print("[DEBUG] request.content_type:", request.content_type)

    if "image" not in request.files:
        print("[ERROR] 'image' not in request.files")
        return jsonify({"error": "No valid image uploaded"}), 400

    file = request.files["image"]
    style = request.form.get("style", "")

    print("[DEBUG] Uploaded filename:", file.filename)

    if file.filename == "":
        print("[ERROR] Empty filename")
        return jsonify({"error": "Empty filename"}), 400

    try:
        img = Image.open(file.stream).convert("RGB")
        print("[INFO] Image loaded and converted to RGB")

        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        b64_img = base64.b64encode(buffered.getvalue()).decode()
        image_mime = "image/jpeg"

        print("[INFO] Encoded image to base64")

        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": f"You are an art critic specializing in {style}."},
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:{image_mime};base64,{b64_img}"}},
                        {"type": "text", "text": "Please critique this artwork."}
                    ]
                }
            ],
            max_tokens=500
        )

        print("[INFO] OpenAI API call successful")
        return jsonify({"critique": response.choices[0].message["content"]})

    except Exception as e:
        print("[ERROR] Exception during processing:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

