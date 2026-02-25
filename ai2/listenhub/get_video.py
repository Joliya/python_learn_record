

import os
from dotenv import load_dotenv
import requests


load_dotenv()

listenhub_api_key = os.getenv("LISTENHUB_API_KEY")

def get_video(episode_id):
    """
    https://api.marswave.ai/openapi/v1/podcast/episodes/{episode_id}
    """
    url = f"https://api.marswave.ai/openapi/v1/podcast/episodes/{episode_id}"
    headers = {
        "Authorization": f"Bearer {listenhub_api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    return response.json()["data"]


print(get_video("68f72e6fb5c163dd5b05181c"))
