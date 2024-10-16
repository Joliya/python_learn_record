# import pandas as pd

# splits = {'train': 'train_datasets.jsonl', 'validation': 'validation_datasets.jsonl', 'test': 'test_datasets.jsonl'}
# df = pd.read_json("hf://datasets/FreedomIntelligence/huatuo_encyclopedia_qa/" + splits["train"], lines=True)

# print(df)



# from datasets import load_dataset

# ds = load_dataset("FreedomIntelligence/huatuo_encyclopedia_qa")


# from huggingface_hub import hf_hub_download
# import pandas as pd

# REPO_ID = "huatuo_encyclopedia_qa"
# FILENAME = "ai/data.csv"

# dataset = pd.read_csv(
#     hf_hub_download(repo_id=REPO_ID, filename=FILENAME, repo_type="dataset")
# )


import os
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
model_list = client.models.list()
for model in model_list:
    print(model.id)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "write a haiku about ai"}
    ],
    response_format={ "type": "json_object" }
)

print(completion.choices[0].message.content)
