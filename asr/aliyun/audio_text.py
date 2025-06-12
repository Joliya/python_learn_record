import json
from urllib import request
from http import HTTPStatus

from dashscope.audio.asr import Transcription

# 若没有将API Key配置到环境变量中，需将下面这行代码注释放开，并将apiKey替换为自己的API Key
# dashscope.api_key = "apiKey"

task_response = Transcription.async_call(
    model='paraformer-v2',
    file_urls=[
        'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav',
        # 'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav'
    ],
    diarization_enabled=True,
    language_hints=['zh', 'en'])

transcription_response = Transcription.wait(
    task=task_response.output.task_id)

if transcription_response.status_code == HTTPStatus.OK:
    for transcription in transcription_response.output['results']:
        url = transcription['transcription_url']
        result = json.loads(request.urlopen(url).read().decode('utf8'))
        print(json.dumps(result, indent=4, ensure_ascii=False))
    print('transcription done!')
else:
    print('Error: ', transcription_response.output.message)