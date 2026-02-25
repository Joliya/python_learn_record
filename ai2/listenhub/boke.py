import os

from dotenv import load_dotenv


load_dotenv()


listenhub_api_key = os.getenv("LISTENHUB_API_KEY")


import requests

def create_dual_podcast(query, speaker_ids, mode="deep"):
    """
    创建双人播客
    
    Args:
        query: 播客主题
        speaker_ids: 音色ID列表（2个）
        mode: 播客模式（quick/deep/debate）
    """
    url = "https://api.marswave.ai/openapi/v1/podcast/episodes"
    headers = {
        "Authorization": f"Bearer {listenhub_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "query": query,
        "speakers": [{"speakerId": sid} for sid in speaker_ids],
        "language": "zh",
        "mode": mode
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def create_flowspeech(text, speaker_id, mode="direct"):
    """
    创建 FlowSpeech 语音
    
    Args:
        text: 要转换的文本
        speaker_id: 音色ID（从音色列表接口获取）
        mode: smart（AI优化）或 direct（文本直接转换）
    """
    url = "https://api.marswave.ai/openapi/v1/flowspeech/episodes"
    headers = {
        "Authorization": f"Bearer {listenhub_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "sources": [{"type": "text", "content": text}],
        "speakers": [{"speakerId": speaker_id}],
        "language": "zh",
        "mode": mode
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()


query = """绮丽丝语丝素蛋白是中国原创医美产品，也是唯一对海外发达国家进行技术授权出口的中国美学产品，
已与韩国 GCS 株式会社达成全球授权合作，多位明星艺人使用，且有中、日、韩及中国台湾地区知名医美专家组成的专业团队支持，还设立了复向美学再生研究中心，
其核心功效包括去除眼周细纹、额纹、眉间纹等浅层静态纹并保留自然微表情、进行屏障修复与敏感肌维稳（改善炎症、术后泛红等问题）以及作为胶原蛋白与弹性蛋白双效刺激剂促进皮肤组织再生，
产品优势在于安全性高（天然蚕丝提取，氨基酸与人体蛋白高度同源，过敏率极低，再生无炎症介质释放，
降解后为氨基酸无残留，适配敏感肌等）、0 恢复期、7 天起效且 14-20 天达效果巅峰、长效维持 4-6 个月，同时兼容性强（可联用或替代胶原、水光等，也能与动能素、肉毒素复配或结合光电项目），
使用上全脸每次 2-3 支（单次不超 7 支）、眼周每次 1-2 支，有连续 3 个月每月 1 次休息 3 个月再重复的叠加套餐（年 6 次）和每 2-3 个月 1 次的均匀套餐（年 4-6 次），
复配可加生理盐水与非交联玻尿酸，水光机打 0.6-1.0mm 真皮层（渗血最佳）且近眼周需专业医生操作，适用有抗皱紧致、静态纹改善需求的全脸水光高端人群、眼周衰老人群及追求自然医美、皮肤敏感的求美者。
播客主题：关于眼周细纹，薇旖美和绮丽丝语丝素蛋白的区别，突出绮丽丝语丝素蛋白的优势。
"""



# 使用示例
result = create_dual_podcast(
    query,
    ["zhibonusheng-7b0dbae2", "gaoqing3-bfb5c88a"],
    "quick"
)
print("Episode ID:", result["data"]["episodeId"])

# result = create_flowspeech(query, "CN-Man-Beijing-V2", "direct")
# print("Episode ID:", result["data"]["episodeId"])
