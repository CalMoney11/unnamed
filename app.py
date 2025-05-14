from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import prompts
import base64
from werkzeug.utils import secure_filename

client = OpenAI(api_key=os.getenv("API_Key_Calv"))

app = Flask(__name__)
CORS(app, origins=["https://unnamed-dev2.github.io"])

UPLOAD_FOLDER = "uploads"
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB limit
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_image_to_base64(filepath):
    with open(filepath, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

@app.route("/api/critique", methods=["POST"])
def critique():
    try:
        prompt = request.form.get("prompt", "")
        style = request.form.get("style", "surrealism")
        file = request.files.get("image")

        if not file or not allowed_file(file.filename):
            return jsonify({"error": "No valid image uploaded"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        base64_image = encode_image_to_base64(filepath)
        user_prompt = prompts.generate_prompt(prompt, style)

        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": prompts.system_message},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=800,
            timeout=60
        )

        critique = response.choices[0].message.content
        return jsonify({"critique": critique})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
