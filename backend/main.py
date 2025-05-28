import functions_framework
from flask import request, jsonify, make_response
from werkzeug.utils import secure_filename
import openai
import os
import base64
import tempfile
from prompts import system_message, generate_prompt, format_openai_messages

openai.api_key = os.getenv("OPENAI_API_KEY")

@functions_framework.http
def generate_art_critique(request):
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Max-Age'] = '3600'
        return response

    try:
        # Validate input
        if 'file' not in request.files:
            return make_json_response({"error": "No image uploaded"}, 400)

        file = request.files['file']
        critique_type = request.form.get("prompt", "")
        style = request.form.get("style", "constructive")

        if not critique_type:
            return make_json_response({"error": "No critique prompt provided"}, 400)

        # Save image to a temp file
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=filename) as tmp:
            file.save(tmp.name)
            image_path = tmp.name

        # Encode image to base64
        with open(image_path, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode("utf-8")

        # Generate prompt and messages
        user_prompt = generate_prompt(critique_type, style)
        messages = [
            {"role": "system", "content": system_message},
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
        ]

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=500
        )

        result = response.choices[0].message["content"]

        # Clean up file
        os.remove(image_path)

        return make_json_response({"response": result})

    except Exception as e:
        return make_json_response({"error": str(e)}, 500)


def make_json_response(data, status=200):
    response = make_response(jsonify(data), status)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
