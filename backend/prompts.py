# prompts.py

system_message = "You are a helpful and professional art critique assistant. Respond concisely, clearly, and constructively."

def generate_prompt(art_description: str, critique_style: str = "constructive"):
    """
    Generate a formatted prompt for the OpenAI API.

    Parameters:
        art_description (str): A short description or title of the artwork.
        critique_style (str): The tone or format of critique (e.g., 'constructive', 'professional', 'casual').

    Returns:
        str: A prompt string ready for API input.
    """
    return (
        f"Please provide a {critique_style} critique for the following artwork:\n"
        f"Description: {art_description}\n"
        f"Include strengths, areas for improvement, and questions the artist might consider."
    )
