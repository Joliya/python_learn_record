from dotenv import load_dotenv
import os
import requests


load_dotenv()


listenhub_api_key = os.getenv("LISTENHUB_API_KEY")

def get_voice_list():
    url = "https://api.marswave.ai/openapi/v1/speakers/list?language=zh"
    headers = {
        "Authorization": f"Bearer {listenhub_api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()["data"]


print(get_voice_list())