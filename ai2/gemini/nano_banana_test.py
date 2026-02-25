from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from typing import Optional, List
import os
from dotenv import load_dotenv

load_dotenv()

def edit_image_from_model(
    prompt: str, image_url: str, model: str = 'nano-banana', 
    api_key: str = os.getenv("GEMINI_API_KEY"), base_url: str = 'https://api.zoopcool.com'
) -> Optional[List[str]]:
    """
    通过代理网关调用图片编辑模型（如 nano-banana）
    
    Args:
        prompt: 图片编辑提示词
        image_url: 原始图片URL
        model: 模型枚举
        api_key: API密钥
        base_url: 基础URL
        
    Returns:
        str: 编辑后的图片URL
    """
    import http.client
    import json
    
    conn = http.client.HTTPSConnection(base_url.replace("https://", "").replace("http://", ""))
    payload = json.dumps({
        "prompt": prompt,
        "model": model,
        "image_urls": [image_url],
        "aspect_ratio": '2:3'
    })
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1/images/generations", payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    response_data = json.loads(data.decode("utf-8"))
    
    if 'data' in response_data and len(response_data['data']) > 0:
        return [item.get('url') for item in response_data['data']]
    
    return None


p = """
编辑图片，将图中左边人物完全移除下眼睑睫毛根部的卧蚕（眼苔），使下眼睑区域呈现平整、平滑的状态，无明显凸起
"""

