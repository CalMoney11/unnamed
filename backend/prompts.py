system_message = "You are a helpful art critique assistant."

def generate_prompt(art, style):
    return f"Please provide a {style} critique of the following piece: {art}"
