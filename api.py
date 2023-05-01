import os

import openai
import requests
from facebook_business import FacebookAdsApi

from answer_ai import settings

openai.api_key = os.getenv("OPENAI_API_KEY")

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

app_id = settings.FACEBOOK_APP_ID
app_secret = settings.FACEBOOK_APP_SECRET
access_token = "EAARX4c7FQAYBAMsQzhNCkYG7IDHWuL6LEZCn0pVwQ1wnhL2sjkW2TeiyZAdnZCM32KmarZAmYpivTGmwwsnpqUEw7lQrUmcU6JB4TcfSBKguBVrEI38ITDoi01x7kp4BYimEQLbBVC5LXp3CpCF1AmyJT01ZAaM4MvAPy832KlZAH5wpOZCSN1KUVk6fD5sZCXWjmdzBzW0iXsDifDT2HOsDcXbzF1ZArfRwZD"
FacebookAdsApi.init(app_id, app_secret, access_token)

params = {
    "search_terms": "beauté",
    "ad_reached_countries": "FR",
    "fields": "ad_creative_body,ad_creative_link_caption,ad_creative_link_description,ad_creative_link_title,"
              "ad_creative_link_url,ad_snapshot_url,impressions",
    "limit": 10
}

# URL de l'API Facebook Ad Library
url = "https://graph.facebook.com/v16.0/ads_archive"

# Envoi de la requête API
response = requests.get(url, params=params)



if __name__ == "__main__":
    # print(ai_response('Build ai platform', 10, "text-davinci-003", 0.9))
    # print(chat_completion('Build ai platform'))

    fields = [
        'ad_creative_body',
        'ad_creative_link_caption',
        'ad_creative_link_description',
        'ad_creative_link_title',
        'ad_delivery_start_time',
        'ad_snapshot_url',
        'ad_creation_time',
        'ad_creative_link_url',
        'ad_delivery_stop_time', ]

    params = {
        'search_terms': 'choose',
        'ad_reached_countries': ['US'],
        'ad_active_status': 'ALL',
        'ad_type': 'POLITICAL_AND_ISSUE_ADS',
        'fields': fields,
    }

    # print(fb_ad_library(params))

