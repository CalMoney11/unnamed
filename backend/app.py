from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import prompts
import base64
from werkzeug.utils import secure_filename

# === Setup ===
client = OpenAI(api_key=os.getenv("API_Key_Calv"))

app = Flask(__name__)
CORS(app, origins=["https://unnamed-dev2.github.io"])

UPLOAD_FOLDER = "uploads"
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === Helpers ===
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_image_to_base64(filepath):
    with open(filepath, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# === Routes ===
@app.route("/api/critique", methods=["POST"])
def critique():
    try:
        # Read form inputs
        art = request.form.get("art", "")
        style = request.form.get("style", "surrealism")
        file = request.files.get("file", None)

        print("✅ Form data received:", art[:100], style)

        # Validate uploaded file
        if not file or not allowed_file(file.filename):
            print("❌ Invalid or missing file.")
            return jsonify({"error": "No valid image uploaded"}), 400

        # Save securely
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        print("✅ File saved:", filepath)

        # Convert image to base64
        base64_image = encode_image_to_base64(filepath)
        print("✅ Image encoded")

        # Prompt construction
        user_prompt = prompts.generate_prompt(art, style)
        print("🧠 Prompt ready")

        # OpenAI API call
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
        print("✅ Critique complete")
        return jsonify({"critique": critique})

    except Exception as e:
        print("❌ Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500

    finally:
        # Cleanup
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
            print("🧹 File removed:", filepath)

# === Entrypoint for Cloud Run ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
