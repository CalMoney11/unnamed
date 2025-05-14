from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import prompts
import base64
from werkzeug.utils import secure_filename

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("API_Key_Calv"))

# Create Flask app
app = Flask(__name__)
CORS(app, origins=["https://unnamed-dev2.github.io"])

# Upload settings
UPLOAD_FOLDER = "uploads"
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Utility: Check file extension
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

# Utility: Encode image for OpenAI
def encode_image_to_base64(filepath):
    with open(filepath, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Main endpoint
@app.route("/api/critique", methods=["POST"])
def critique():
    try:
        prompt = request.form.get("prompt", "").strip()
        style = request.form.get("style", "surrealism").strip()
        file = request.files.get("image")

        # Validate file
        if not file or not allowed_file(file.filename):
            return jsonify({"error": "No valid image uploaded. Must be .jpg, .jpeg, or .png"}), 400

        # Save file safely
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Encode image and generate prompt
        base64_image = encode_image_to_base64(filepath)
        user_prompt = prompts.generate_prompt(prompt, style)

        # Logging for debug
        print(f"[INFO] User prompt: {user_prompt}")
        print(f"[INFO] Image base64 length: {len(base64_image)}")

        # Call OpenAI
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
        print(f"[ERROR] {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            if 'filepath' in locals() and os.path.exists(filepath):
                os.remove(filepath)
        except Exception as cleanup_error:
            print(f"[CLEANUP ERROR] {cleanup_error}")

# Start server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
