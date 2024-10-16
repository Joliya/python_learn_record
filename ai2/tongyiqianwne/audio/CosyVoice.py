
import os
import dashscope
from dashscope.audio.tts_v2 import *


# 将your-dashscope-api-key替换成您自己的API-KEY
dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")
model = "cosyvoice-v1"
voice = "longxiaochun"


synthesizer = SpeechSynthesizer(model=model, voice=voice)
audio = synthesizer.call("宝，在干嘛呢？")
print('requestId: ', synthesizer.get_last_request_id())
with open('/Users/zhangjinpeng/workspace/python_learn_record/output.mp3', 'wb') as f:
    f.write(audio)