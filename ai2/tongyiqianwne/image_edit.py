from gradio_client import Client, handle_file

client = Client("Qwen/Qwen-Image-Edit-2511")
result = client.predict(
	images=[{"image":handle_file('https://picaso-static.oss-cn-beijing.aliyuncs.com/cases/images/84cc8e5f-9dc6-4590-97f6-3ad6e089a2b1.png'),"caption":None}],
	prompt="将图中人物面部美白、皮肤精致、色斑减少",
	seed=0,
	randomize_seed=True,
	true_guidance_scale=4,
	num_inference_steps=40,
	height=256,
	width=256,
	rewrite_prompt=True,
	api_name="/infer"
)
print(result)