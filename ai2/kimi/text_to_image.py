import os
import logging as logger
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 1. 把 KEY 写环境变量里（也可以直接写字符串）
KIMI_API_KEY = os.getenv("KIMI_API_KEY")
# 2. 指定月之暗面接口地址
client = OpenClient(
    api_key=KIMI_API_KEY,
    base_url="https://api.moonshot.cn/v1"
)

def text_to_image(prompt: str, save_path: str = "output.png"):
    """输入一段文字，保存生成图片到本地"""
    response = client.images.generate(
        model="k2-high",      # 2025-08 开放的文生图模型
        prompt=prompt,
        n=1,
        size="1024x1024",     # 可选 512×512 / 1024×1024 / 1440×1440
        response_format="b64_json"
    )
    import base64
    img_data = base64.b64decode(response.data[0].b64_json)
    with open(save_path, "wb") as f:
        f.write(img_data)
    print(f"已保存 → {os.path.abspath(save_path)}")

if __name__ == "__main__":
    text = input("请输入想生成的画面描述：")
    text_to_image(text)
