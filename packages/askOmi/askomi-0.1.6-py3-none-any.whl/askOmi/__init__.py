import os
from google import genai


def askOmi(error):

    api_key = "AIzaSyATDPGbokzoJaBm9CU56GbvJT-1rCd75ls"
    
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=error
    )

    print(response.text)
