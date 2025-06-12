from modelscope import snapshot_download
model_dir = snapshot_download('moonshotai/Kimi-Audio-7B-Instruct',
                              cache_dir="./models")
