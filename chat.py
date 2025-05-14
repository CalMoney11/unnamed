import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Initialize OpenAI client with project key and optional organization
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),           # Your sk-proj-... key
    organization=os.getenv("OPENAI_ORG_ID"),       # Optional: org ID if required
    project=os.getenv("OPENAI_PROJECT_ID")         # Required: the project ID if access is scoped
)

while True:
    prompt = input("\n🟡 Ask something (or 'quit' to exit): ")
    if prompt.lower() in ["quit", "exit"]:
        break

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        print("\n🤖", response.choices[0].message.content.strip())

    except Exception as e:
        print("❌ Error:", e)

