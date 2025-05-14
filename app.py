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

    file = request.files["image"]
    style = request.form.get("style", "")
    if file.filename == "":
        print("[ERROR] Empty filename")
        return jsonify({"error": "Empty filename"}), 400

    try:
        from PIL import Image
        import base64
        from io import BytesIO

        img = Image.open(file.stream).convert("RGB")
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        b64_img = base64.b64encode(buffered.getvalue()).decode()
        image_mime = "image/jpeg"

        print("[INFO] Sending image to OpenAI API...")

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

        print("[INFO] OpenAI response received.")
        return jsonify({"critique": response.choices[0].message["content"]})
    
    except Exception as e:
        print("[EXCEPTION] An error occurred:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

