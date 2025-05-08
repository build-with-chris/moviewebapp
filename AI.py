import requests
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")


def ask_movie_assistent(user_input):
    url = "https://cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com/v1/chat/completions"

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant who gives sharp, concise answers. "
                           "Your expertise is focused on movies and movie recommendations."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        "model": "gpt-4o",
        "max_tokens": 100,
        "temperature": 0.8
    }
    headers = {
        "x-rapidapi-key": OPENAI_KEY,
        "x-rapidapi-host": "cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]