import os
# Install SDK:  pip install 'volcengine-python-sdk[ark]' .
from volcenginesdkarkruntime import Ark
from volcenginesdkarkruntime.types.images import SequentialImageGenerationOptions 

client = Ark(
    # The base URL for model invocation .
    base_url="https://ark.cn-beijing.volces.com/api/v3", 
    # Get API Key：https://console.volcengine.com/ark/region:ark+cn-beijing/apikey
    api_key='', 
)
 
## 泪沟
# imagesResponse = client.images.generate(
#     # Replace with Model ID .
#     model="doubao-seedream-4-0-250828",
#     prompt="""一张中国女性医美治疗前后对比图，参考图中人物眼部下方泪沟特征。
#     脸型：小V脸
#     25岁，自然光线下，正面平视角度。
#     左侧为治疗前：眼部下方有明显痕迹，泪沟明显，呈凹陷阴影状，略显暗沉；
#     右侧为治疗后：泪沟被透明质酸填充，凹陷平整，眼下皮肤饱满平滑，无淤青或红肿，肤色与左侧完全一致。
#     整体风格真实自然，符合东方审美，柔焦人像摄影，8K画质，专业医疗对比图标准。
#     关键词：同一人像，相同光线，相同角度，相同肤色参数，自然减龄效果，不露痕迹的微整形，中国人面部特征。""",
#     size="4k",
#     response_format="url",
#     watermark=False,
#     image=['https://midjourney-plus.oss-us-west-1.aliyuncs.com/sora/ba4d3fa0-445f-45eb-8f94-1dd9daa91404.png'],
#     sequential_image_generation='auto',
#     sequential_image_generation_options=SequentialImageGenerationOptions(max_images=5)
# )  
 
# print(imagesResponse.data[0].url)

## 卧蚕
# imagesResponse = client.images.generate(
#     # Replace with Model ID .
#     model="doubao-seedream-4-0-250828",
#     prompt="""同一位中国女性的医美前后对比图，镜头离远一些，露出脖子，。左右分屏，25岁，鹅蛋脸，肤如凝脂，不要有任何文字。左侧：参考图1中左侧人物眼部效果，无卧蚕，眼睛下面皮肤平整，黑色圆领短袖，头发呈马尾状。右侧：参考图1中右侧人物眼部效果，有卧蚕，眼睛下面皮肤饱满，白色圆领短袖，头发呈披肩状。鼻唇与左侧完全相同。核心要求：前后必须同一个人，前后背景在不同的地方，可以是人物自拍或者他拍""",
#     size="2496x1664",
#     response_format="url",
#     watermark=False,
#     image=['https://picaso-static.oss-cn-beijing.aliyuncs.com/cases/images/20251117-163009.jpeg'],
#     sequential_image_generation='auto',
#     sequential_image_generation_options=SequentialImageGenerationOptions(max_images=5),
#     seed=-1
# )  

# print(imagesResponse.data[0].url)


## 卧蚕单个（before）
# imagesResponse = client.images.generate(
#     # Replace with Model ID .
#     model="doubao-seedream-4-0-250828",
#     prompt="""生成一位中国女性的照片，镜头离远一些，。25岁，鹅蛋脸，肤如凝脂，不要有任何文字。参考图1中人物眼部特征，眼周平整无卧蚕。图片背景自然，可以是家里、办公室、公园等场景。人物要求展示胸部及以上""",
#     size="1728x2304",
#     response_format="url",
#     watermark=False,
#     image=['https://picaso-static.oss-cn-beijing.aliyuncs.com/cases/images/20251117-162328.jpeg'],
#     seed=-1
# )

# print(imagesResponse.data[0].url)


## 卧蚕单个（after）
# imagesResponse = client.images.generate(
#     # Replace with Model ID .
#     model="doubao-seedream-4-0-250828",
#     prompt="""生成一位中国女性的照片，镜头离远一些，。25岁，鹅蛋脸，肤如凝脂，不要有任何文字。参考图1中人物眼部特征，眼周饱满有卧蚕。图片背景自然，背景是家里。人物要求展示胸部及以上，浅色衣服，头发披肩，头发颜色为棕色""",
#     size="1728x2304",
#     response_format="url",
#     watermark=False,
#     image=['https://picaso-static.oss-cn-beijing.aliyuncs.com/cases/images/20251117-162332.jpeg'],
#     seed=-1
# )

# print(imagesResponse.data[0].url)


## 眉弓单个（before）
# imagesResponse = client.images.generate(
#     # Replace with Model ID .
#     model="doubao-seedream-4-0-250828",
#     prompt="""生成一位中国女性的侧脸照片，镜头离远一些，。25岁，鹅蛋脸，肤如凝脂，不要有任何文字。参考图1中人物眉弓特征，眉弓平坦、眶上缘平缓，眉弓与鼻梁平齐。图片背景自然，背景是在家里卧室。人物要求展示肩部及以上，浅色衣服，头发披肩，头发颜色为棕色，人物侧面展示""",
#     size="1728x2304",
#     response_format="url",
#     watermark=False,
#     image=['https://picaso-static.oss-cn-beijing.aliyuncs.com/cases/images/20251118-115026.jpeg'],
#     seed=-1
# )

# print(imagesResponse.data[0].url)

## 眉弓单个（after）
# imagesResponse = client.images.generate(
#     # Replace with Model ID .
#     model="doubao-seedream-4-0-250828",
#     prompt="""生成一位中国女性的照片，镜头离远一些，展示人物标准侧脸。25岁，鹅蛋脸，肤如凝脂，不要有任何文字。参考图1中人物眉弓特征，眉弓发育良好、明显突出。图片背景自然，背景是在家里卧室。人物要求展示肩部及以上，深色衣服，头发扎起，头发颜色为棕色""",
#     size="1728x2304",
#     response_format="url",
#     watermark=False,
#     image=['https://picaso-static.oss-cn-beijing.aliyuncs.com/cases/images/20251118-115033.jpeg'],
#     seed=-1
# )

# print(imagesResponse.data[0].url)


## 丰唇对比
# imagesResponse = client.images.generate(
#     # Replace with Model ID .
#     model="doubao-seedream-4-0-250828",
#     prompt="""生成一位中国女昨晚丰唇项目的前后对比照片，镜头离远一些，展示人物正面。25岁，鹅蛋脸，肤如凝脂，不要有任何文字。左边：术前：参考图1中人物唇部特征，嘴唇薄、缺乏立体感，头发扎起，头发颜色为棕色，衣服为浅色，背景在客厅。右边：术后：参考图2唇部特征，嘴唇饱满、立体感强，唇形清晰，头发扎起，头发颜色为棕色，衣服为深色，背景在卧室。人物要求before、after 发型、衣服、背景要不一样，保证前后是一个人，不要有任何文字""",
#     size="2496x1664",
#     response_format="url",
#     watermark=False,
#     image=['https://picaso-static.oss-cn-beijing.aliyuncs.com/cases/images/20251118-150157.jpeg', 'https://picaso-static.oss-cn-beijing.aliyuncs.com/cases/images/20251118-145044.jpeg'],
#     seed=1
# )

# print(imagesResponse.data[0].url)


## 轮廓对比
# imagesResponse = client.images.generate(
#     # Replace with Model ID .
#     model="doubao-seedream-4-0-250828",
#     prompt="""生成一位中国女性做面部轮廓提升项目的前后对比照片，镜头离远一些，展示人物正面。
#     25岁，鹅蛋脸，肤如凝脂，不要有任何文字。
#     左边：术前：参考图1中人物脸型特征，太阳穴凹陷，面颊凹陷，外轮廓线条明显不流畅，凹凸明显，头发扎起，头发颜色为棕色，衣服为浅色，背景在客厅。
#     右边：术后：参考图2面部轮廓特征，太阳穴面颊饱满，轮廓线条流畅，头发扎起，头发颜色为黑色，衣服为深色，背景在卧室。
#     人物要求before、after 发型、衣服、背景要不一样，保证前后是一个人，不要有任何文字
#     特别注意：人物不要和参考图中一样""",
#     size="2496x1664",
#     response_format="url",
#     watermark=False,
#     image=['https://picaso-static.oss-cn-beijing.aliyuncs.com/cases/images/20251118-163053.jpeg', 'https://picaso-static.oss-cn-beijing.aliyuncs.com/cases/images/20251118-163056.jpeg'],
#     seed=1
# )

# print(imagesResponse.data[0].url)



## 轮廓对比
imagesResponse = client.images.generate(
    # Replace with Model ID .
    model="doubao-seedream-4-0-250828",
    prompt="""在原图上用白色细线画出 E-line（审美平面线），即从鼻尖画一条直线到下巴尖，展示嘴唇与这条线的位置关系。不要改变原图的其他部分，只添加这条白色参考线。""",
    size="2496x1664",
    response_format="url",
    watermark=False,
    image=['https://picaso-public.oss-accelerate.aliyuncs.com/test/face_report/pyz-cm.jpg'],
)

print(imagesResponse.data[0].url)
