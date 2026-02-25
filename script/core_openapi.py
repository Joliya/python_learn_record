import base64
import hashlib
import hmac
import json
import random
import time
import requests
import secrets

# X_APP_ID = 'app_98f38e43a710d1f3443e87b6a816'
# app_secret = '3b474634b4188be71fc43aa8d9b22cf2994de2d6668507cdedeaa515dcc2eefd'
# X_APP_ID = 'app_8f68b674113b844a8f94a7bb7288'
# app_secret = '891a4aad574cbba8c2532eb1e30116fcc6d553044dac121e81f23f5b7281bd36'

# 静和线上
# X_APP_ID = 'app_3eb9472457c411d97d8d14f5b141'
# app_secret = 'b6c9dd4d1cc01d29ebb9a981651cea97cc279809eac75c619ca34366e9f375cf'

# 千数
X_APP_ID = 'app_8f68b674113b844a8f94a7bb7288'
app_secret = '891a4aad574cbba8c2532eb1e30116fcc6d553044dac121e81f23f5b7281bd36'

# domain = 'https://open.picaso.tech'
domain = 'https://open.qianshu.tech'
# domain = 'http://127.0.0.1:8000'

def generate_app_id() -> str:
    """
    生成应用ID

    Returns:
        32位随机字符串
    """
    return f"app_{secrets.token_hex(14)}"


def generate_app_secret() -> str:
    """
    生成应用密钥

    Returns:
        64位随机字符串
    """
    return secrets.token_hex(32)


def generate_signature(
    app_secret: str,
    method: str,
    path: str,
    timestamp: int,
    nonce: str,
    body: str
) -> str:
    """
    生成请求签名

    签名规则：
    1. 构造待签名字符串：{HTTP方法}\n{请求路径}\n{时间戳}\n{随机串}\n{请求体}
    2. 使用 HMAC-SHA256 算法签名
    3. 对签名结果进行 Base64 编码

    Args:
        app_secret: 应用密钥
        method: HTTP 方法（如 POST、GET）
        path: 请求路径（如 /report_api/v1/create）
        timestamp: 时间戳（秒）
        nonce: 随机串
        body: 请求体（空则为空字符串）

    Returns:
        Base64 编码的签名字符串
    """
    # 构造待签名字符串
    string_to_sign = f"{method}\n{path}\n{timestamp}\n{nonce}\n{body}"

    # HMAC-SHA256 签名
    signature = hmac.new(
        key=app_secret.encode("utf-8"),
        msg=string_to_sign.encode("utf-8"),
        digestmod=hashlib.sha256
    ).digest()

    # Base64 编码
    return base64.b64encode(signature).decode("utf-8")


def create_report():
    method = 'POST'
    

    path = '/open/report_api/v1/create'
    timestamp = int(time.time())
    nonce = generate_app_id()

    # data = {
    #     'external_user_id': '1',
    #     'front_photo_url': 'https://picaso-public.oss-cn-beijing.aliyuncs.com/test/avatar/7/29e23bd1cd164707b3b75f1f82ffab54.jpg',
    #     'side_photo_url': 'https://picaso-public.oss-cn-beijing.aliyuncs.com/test/avatar/7/5b2e270acd6742d29ea04c2d6dffb05a.jpg',
    #     'improve_demand': {"symptom_list": [{"category": "面部轮廓", "tag_list": ["太阳穴凹陷"], "request": "太阳穴"}, {"category": "皮肤质地", "tag_list": ["毛孔粗大", "痘印/痘坑"], "request": "改善痘印痘坑"}, {"category": "凹陷", "tag_list": ["太阳穴凹陷"], "request": ""}, {"category": "唇部与口周症状", "tag_list": ["人中过长"], "request": ""}], "user_profile": {"history_treatment": ["没做过"], "pain_tolerance": "完全不怕"}},
    #     'user_phone': "",
    #     'consultant_phone': "",
    #     'callback_url': "",
    #     'extra': {},
    # }

    data = {
        "external_user_id": "1", 
        "front_photo_url": "https://picaso-public.oss-cn-beijing.aliyuncs.com/prod/avatar/2982/17b783820cbe4f1dbe947a7128ea3afc.jpg", 
        "side_photo_url": "https://picaso-public.oss-cn-beijing.aliyuncs.com/prod/avatar/2982/e7ba4f33ff744485bf5f95a02bfaf05b.jpg", 
        "user_phone": "", 
        "consultant_phone": "", 
        "callback_url": "", 
        "extra": {}}

    body = json.dumps(data)
    # body = body.encode('utf-8')
    X_SIGNATURE = generate_signature(app_secret, method, path, timestamp, nonce, body)
    header = {
        'X-App-Id': X_APP_ID,
        'x-Timestamp': str(timestamp),
        'x-Nonce': nonce,
        'x-Signature': X_SIGNATURE,
        'Content-Type': 'application/json',
    }
    print(f"body: {body} \n request.method: {method} \n request.path: {path} \n timestamp: {timestamp} \n nonce: {nonce}")

    response = requests.post(
        f'{domain}/open/report_api/v1/create',
        headers=header,
        data=json.dumps(data),
    )

    print(response.json())


def query_report_status(report_id: int):
    method = 'GET'
    path = f'/open/report_api/v1/{report_id}/status'
    timestamp = int(time.time())
    nonce = generate_app_id()

    data = {}

    body = json.dumps(data)
    # body = body.encode('utf-8')
    X_SIGNATURE = generate_signature(app_secret, method, path, timestamp, nonce, body)
    header = {
        'X-App-Id': X_APP_ID,
        'x-Timestamp': str(timestamp),
        'x-Nonce': nonce,
        'x-Signature': X_SIGNATURE,
        'Content-Type': 'application/json',
    }
    print(f"body: {body} \n request.method: {method} \n request.path: {path} \n timestamp: {timestamp} \n nonce: {nonce}")

    response = requests.get(
        f'{domain}/{path}',
        headers=header,
        data=json.dumps(data),
    )

    print(response.json())


def query_report_detail(report_id: int):
    method = 'GET'
    path = f'/open/report_api/v1/{report_id}'
    timestamp = int(time.time())
    nonce = generate_app_id()
    data = {}
    body = json.dumps(data)
    X_SIGNATURE = generate_signature(app_secret, method, path, timestamp, nonce, body)
    header = {
        'X-App-Id': X_APP_ID,
        'x-Timestamp': str(timestamp),
        'x-Nonce': nonce,
        'x-Signature': X_SIGNATURE,
        'Content-Type': 'application/json',
    }
    print(f"body: {body} \n request.method: {method} \n request.path: {path} \n timestamp: {timestamp} \n nonce: {nonce}")
    response = requests.get(
        f'{domain}/{path}',
        headers=header,
        data=json.dumps(data),
    )
    print(response.json())


def image_moderation(image_urls: list[str]):
    method = 'POST'
    path = f'/open/report_api/v1/image_moderation'
    timestamp = int(time.time())
    nonce = generate_app_id()
    data = {
        "image_urls": image_urls
    }
    body = json.dumps(data)
    X_SIGNATURE = generate_signature(app_secret, method, path, timestamp, nonce, body)
    header = {
        'X-App-Id': X_APP_ID,
        'x-Timestamp': str(timestamp),
        'x-Nonce': nonce,
        'x-Signature': X_SIGNATURE,
        'Content-Type': 'application/json',
    }
    print(f"body: {body} \n request.method: {method} \n request.path: {path} \n timestamp: {timestamp} \n nonce: {nonce}")
    response = requests.post(
        f'{domain}/{path}',
        headers=header,
        data=json.dumps(data),
    )
    print(response.json())



if __name__ == '__main__':
    create_report()
    # query_report_status(73)
    # query_report_detail(125)
    # image_moderation(["https://oss.chingho.net/facedemo/2026-01-19/1768799640___IMG_8739.JPG",
    # "https://oss.chingho.net/facedemo/2026-01-19/1768799669___IMG_8743.JPG"])
