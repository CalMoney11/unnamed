import functions_framework
from flask import request, jsonify
from werkzeug.utils import secure_filename
import openai
import os
import base64
import tempfile
from prompts import system_message, generate_prompt, format_openai_messages

openai.api_key = os.getenv("OPENAI_API_KEY")

@functions_framework.http
def generate_art_critique(request):
    try:
        # Check for file and fields
        if 'file' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files['file']
        critique_type = request.form.get("prompt", "")
        style = request.form.get("style", "constructive")

        if not critique_type:
            return jsonify({"error": "No critique prompt provided"}), 400

        # Save temp image
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=filename) as tmp:
            file.save(tmp.name)
            image_path = tmp.name

        # Convert to base64
        with open(image_path, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode("utf-8")

        # Build prompt and message
        user_prompt = generate_prompt(critique_type, style)
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ]

        # Call GPT-4 Vision
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=messages + [{
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
            }],
            max_tokens=500
        )

        result = response.choices[0].message["content"]

        # Cleanup
        os.remove(image_path)

        return jsonify({"response": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
