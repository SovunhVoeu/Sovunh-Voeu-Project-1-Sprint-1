"""

Author: Sovunh Voeu
Date: 1/29/2025

"""
import google.generativeai as genai
from pathlib import Path
# import json

def api_model_and_response():
    file_path = Path('YOUR_API_KEY.txt')
    api = file_path.read_text()

    genai.configure(api_key=api)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Deliver the intended prompt to the AI here
    user_input = input("Deliver the intended prompt to the AI here: \n")


    response = model.generate_content(user_input)
    print( "\n" + response.text)

if __name__ == '__main__':
    api_model_and_response()

