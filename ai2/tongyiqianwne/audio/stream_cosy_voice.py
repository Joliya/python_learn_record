# coding=utf-8
#
# Installation instructions for pyaudio:
# APPLE Mac OS X
#   brew install portaudio
#   pip install pyaudio
# Debian/Ubuntu
#   sudo apt-get install python-pyaudio python3-pyaudio
#   or
#   pip install pyaudio
# CentOS
#   sudo yum install -y portaudio portaudio-devel && pip install pyaudio
# Microsoft Windows
#   python -m pip install pyaudio

# 流式文本语音合成，边生成边播放

import os
import time
import pyaudio
import dashscope
from dashscope.api_entities.dashscope_response import SpeechSynthesisResponse
from dashscope.audio.tts_v2 import *

# 将your-dashscope-api-key替换成您自己的API-KEY
dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")
model = "cosyvoice-v1"
voice = "longxiaochun"


class Callback(ResultCallback):
    _player = None
    _stream = None
    _audio_file = None

    def on_open(self):
        print("websocket is open.")
        self._player = pyaudio.PyAudio()
        self._stream = self._player.open(
            format=pyaudio.paInt16, channels=1, rate=22050, output=True
        )
        self._audio_file = open("audio.pcm", "wb")

    def on_complete(self):
        print("speech synthesis task complete successfully.")
        if self._audio_file:
            self._audio_file.close()

    def on_error(self, message: str):
        print(f"speech synthesis task failed, {message}")

    def on_close(self):
        print("websocket is closed.")
        # 停止播放器
        self._stream.stop_stream()
        self._stream.close()
        self._player.terminate()
        if self._audio_file:
            self._audio_file.close()

    def on_event(self, message):
        print(f"recv speech synthsis message {message}")

    def on_data(self, data: bytes) -> None:
        print("audio result length:", len(data))
        self._stream.write(data)

        if self._audio_file:
            self._audio_file.write(data)


callback = Callback()

test_text = [
    "微风轻拂",
    "携来大自然的低语",
    "抚平心灵的波澜",
    "带来无尽的宁静与清新",
    "风，是天空的温柔拥抱"
]

synthesizer = SpeechSynthesizer(
    model=model,
    voice=voice,
    format=AudioFormat.PCM_22050HZ_MONO_16BIT,  
    callback=callback,
)


for text in test_text:
    synthesizer.streaming_call(text)
    time.sleep(0.5)
synthesizer.streaming_complete()
print('requestId: ', synthesizer.get_last_request_id())