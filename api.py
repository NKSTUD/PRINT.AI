import os

import openai
import google.generativeai as genai
import requests
from facebook_business import FacebookAdsApi
from markdown import markdown
from cmarkgfm import markdown_to_html

from answer_ai import settings

openai.api_key = os.getenv("OPENAI_API_KEY")

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

try:
    def ai_response(user_prompt: str, max_tokens: int,
                    model: str, temperature: float, frequency_penalty: float = 0.0):
        response = openai.Completion.create(
            model=model,
            prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=frequency_penalty,
            presence_penalty=0
        )
        total_tokens = response["usage"]["total_tokens"]
        return response["choices"][0]["text"], total_tokens
except ConnectionError as e:
    raise e

try:
    def chat_completion(user_prompt: str):

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are  Print.ai developed by Nouhan Kourouma."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]
except Exception as e:
    raise e


class GeminiChat:
    def __init__(self, prompt: str, model: str = 'gemini-1.5-pro-latest', ):
        self.model = model
        self.prompt = prompt

    def gemini_chat_completion(self):
        model = genai.GenerativeModel(self.model)
        response = model.generate_content({self.prompt}, stream=False)
        response.resolve()

        print(response.text)
        return markdown_to_html(response.text)

    def gemini_token_count(self):
        total_token = genai.GenerativeModel(self.model).count_tokens(self.prompt)
        return total_token


if __name__ == "__main__":
    print(ai_response('Build ai platform', 10, "text-davinci-003", 0.9))
    print(chat_completion('Build ai platform'))
