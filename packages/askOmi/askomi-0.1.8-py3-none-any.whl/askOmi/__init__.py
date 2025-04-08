import os
from google import genai


def askOmi(error):

    api_key = "AIzaSyATDPGbokzoJaBm9CU56GbvJT-1rCd75ls"
    
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=error
    )
    return response.text

def html(error):
    answer = askOmi(error)

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>css</title>
</head>
<body>
    <br><br><br><br><br><br><br><br><br><br><br><br><br><br>
    <br><br><br><br><br><br><br><br><br><br><br><br><br><br>
    <br><br><br><br><br><br><br><br><br><br><br><br><br><br>
    <br><br><br><br><br><br><br><br><br><br><br><br><br><br>
    <br><br><br><br><br><br><br><br><br><br><br><br><br><br>
    <p>{answer}</p>
</body>
</html>
"""

    with open("output.html", "w") as f:
        f.write(html_content)

    
