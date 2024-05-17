import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Sunbird API endpoint for translation
TRANSLATION_API_URL = "https://api.sunbird.ai/tasks/nllb_translate"

# Language codes for the Local Languages
LANGUAGE_CODES = {
    "English": "eng",
    "Luganda": "lug",
    "Runyankole": "nyn",
    "Acholi": "ach",
    "Ateso": "teo",
    "Lugbara": "lgg"
}

# Function to get user input for language selection
def get_language(prompt):
    while True:
        lang = input(prompt).strip().title()  # Convert input to title case for consistency
        if lang in LANGUAGE_CODES:
            return lang
        else:
            print("Invalid language. Please choose from the provided options.")

# Function to call Sunbird translation API
def translate_text(source_lang, target_lang, text):
    access_token = os.getenv("AUTH_TOKEN")
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwYXRyaWNrY21kIiwiYWNjb3VudF90eXBlIjoiRnJlZSIsImV4cCI6NDg2OTE4NjUzOX0.wcFG_GjBSNVZCpP4NPC2xk6Dio8Jdd8vMb8e_rzXOFc",
        "Content-Type": "application/json",
    }
    data = {
        "source_language": LANGUAGE_CODES[source_lang],
        "target_language": LANGUAGE_CODES[target_lang],
        "text": text,
    }
    response = requests.post(TRANSLATION_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        translated_text = response_data.get("output", {}).get("data", {}).get("translated_text")
        if translated_text:
            return translated_text
        else:
            print("Translated text not found in response data.")
            return None
    else:
        print("Translation failed. Please try again later.")
        return None

# Main function
def main():
    # Get source language
    print("Choose the source language:")
    source_lang = get_language("Enter source language: ")

    # Get target language
    print("Choose the target language:")
    target_lang = get_language("Enter target language: ")

    # Ensure target language is different from source language
    while target_lang == source_lang:
        print("Target language can't be the same as source language.")
        target_lang = get_language("Enter target language: ")

    # Get text to translate
    text = input(f"Enter the text to translate (in {source_lang}): ")

    # Translate text
    translated_text = translate_text(source_lang, target_lang, text)

    # Print translated text
    if translated_text:
        print(translated_text)

if __name__ == "__main__":
    main()
