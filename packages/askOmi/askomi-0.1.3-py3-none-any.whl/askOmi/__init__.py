import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def askOmi(error):

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GENAI_API_KEY environment variable not set!")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=error
    )

    print(response.text)
