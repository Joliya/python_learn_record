import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv
import logging as logger

load_dotenv()

ZOOPCOOL_BASE_URL = "https://api.zoopcool.com/v1"
ZOOPCOOL_API_KEY = os.getenv("ZOOPCOOL_API_KEY")


KIMI_BASE_URL = "https://api.moonshot.cn/v1"
KIMI_API_KEY = os.getenv("KIMI_API_KEY")


def get_text_content_from_model(
    prompt: str, model: str = 'kimi-k2-0905-preview', api_key: str = KIMI_API_KEY,
    base_url: str = KIMI_BASE_URL, temperature: float = 0.9
):
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    content = response.choices[0].message.content
    return content


def get_image_from_model(
    prompt: str, model: str = 'gpt-image-1', api_key: str = os.getenv("ZOOPCOOL_API_KEY"),
    base_url: str = "https://api.zoopcool.com/v1", response_format: str = 'url',
    size: str = "1536x1024"
) -> Optional[str]:
    """
    通过代理网关调用图片生成模型
    
    Args:
        prompt: 图片生成提示词
        model: 模型枚举
        api_key: API密钥
        base_url: 基础URL
        response_format: 响应格式，'b64_json' 或 'url'
        size: 图片尺寸
        
    Returns:
        str: base64编码的图片或URL
    """
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.images.generate(
        model=model,
        prompt=prompt,
        n=1,
        size=size,
        quality="high",
        # response_format=response_format
    )
    print(response)
    if response_format == 'b64_json':
        base64_image = response.data[0].b64_json
        return base64_image
    return response.data[0].url


# PROMPT_IMAGE_DESC = """
# Create a realistic before-and-after comparison image of a Chinese woman who has undergone a cosmetic treatment. 
# The image should show two side-by-side portraits: the left side "Before" and the right side "After". 

# Randomly generate a unique and natural-looking Chinese woman in her 20s to 40s, with realistic facial features, hairstyle, and skin tone variation — for example: 
# one might have shoulder-length straight black hair, natural makeup, and warm skin tone; another could have tied hair, clear skin, and gentle expression. 
# Avoid celebrity likeness. Keep the expression neutral and lighting consistent between both sides. 

# Highlight visible improvement in **{target_improvement_area}**, clearly showing the difference between before and after. 
# Ensure the results look natural, not exaggerated — subtle yet noticeable enhancement. 

# Style: hyper-realistic, professional clinic photography, soft daylight, clean background, balanced composition, natural beauty aesthetic.
# Add a soft label "Before" and "After" on each side.
# """


# PROMPT_IMAGE_DESC = """
# Create a hyper-realistic before-and-after comparison image of the **same Chinese woman** who has undergone a cosmetic treatment. 

# The image must show two side-by-side portraits of the same person: 
# the **left side labeled “Before”** and the **right side labeled “After”**. 
# Ensure that both portraits depict the exact same woman — identical facial features, hairstyle, and pose — 
# with consistent lighting, camera angle, and expression, so it clearly looks like a natural transformation of the same person. 

# Randomly generate a realistic and natural-looking Chinese woman aged between 20 and 40, 
# with unique but believable traits (e.g. one might have shoulder-length black hair and light natural makeup, another may have tied hair and soft warm skin tone). 
# Avoid any celebrity likeness or artificial appearance.

# Show visible and natural-looking improvement in **{target_improvement_area}**, 
# clearly showing how the cosmetic treatment enhanced her appearance while maintaining authenticity. 
# The “After” side should look subtly rejuvenated, smoother, or more lifted depending on the treatment area.

# Style: professional aesthetic clinic photography, clean neutral background, soft daylight, high resolution, balanced composition, natural beauty style.
# """


PROMPT_IMAGE_DESC = """
Create a hyper-realistic before-and-after comparison image of the same Chinese woman, shown in two side-by-side selfie portraits. Both portraits should be captured from a natural smartphone front-camera angle (slightly upward or straight-on selfie view).

The two portraits must clearly show the same woman — identical facial structure, hairstyle, hair colour, skin tone (apart from the treated area), expression, and camera angle — as if she took both selfies herself at different times. Except for the face region that falls within the {target_improvement_area}, all other body parts (neck, shoulders, upper torso if visible), hairstyle, clothing and background framing should remain exactly the same in both images.

On the before portrait, her skin tone should be natural and healthy, not overly dark or yellow-toned, so that the improvement in the after portrait is realistic and subtle rather than extreme.

The only visible difference between the “before” and “after” should be the {target_improvement_area} on her face, showing a gentle and believable enhancement due to a cosmetic treatment — not a dramatic or unrealistic transformation. All other facial features, lighting tone, expression, and image quality should remain as consistent as possible.

To make the comparison realistic, place the woman in two different but believable everyday environments — for example, one taken indoors near a window, and the other outdoors or in a softly lit room. The backgrounds should differ naturally but not distract from the subject.

Style: hyper-realistic, high-resolution smartphone selfie, natural daylight, realistic background, subtle improvement, no text or labels.

"""


PROMPT_IMAGE_COMPARE_DESC = """
Create a hyper-realistic before-and-after comparison image of the **same Chinese woman**, captured from a natural **selfie angle** (slightly upward or straight-on front camera perspective).

The image must show two side-by-side portraits of the same person:
the **left side labeled “Before”** and the **right side labeled “After”**.
Both portraits should clearly depict the exact same woman — identical facial structure, hairstyle, pose, expression, lighting, and camera angle — 
as if both photos were taken in the same selfie session, minutes apart. 

Only the **{target_improvement_area}** should show visible improvement due to a cosmetic treatment, while all other facial features and details remain as consistent as possible.  
The “After” side should show a natural, realistic enhancement — subtle yet clearly noticeable — avoiding over-editing or artificial effects.

Randomly generate a natural and realistic-looking Chinese woman aged between 20 and 40, with varied but believable details (e.g. different hair lengths, tones, or natural makeup styles).  
Avoid celebrity resemblance. Keep the lighting soft and balanced, background simple and bright, mimicking smartphone selfie lighting.

Style: hyper-realistic, high-resolution selfie portrait, minimal retouching, aesthetic clinic result comparison, labeled “Before” and “After”.

"""

# text = get_text_content_from_model(PROMPT_IMAGE_DESC)
# logger.info(text)
# print(text)

PROMPT_BEFORE_DESC = """
Create a hyper-realistic portrait of a **Chinese woman**, showing natural facial features that match the following skin or aesthetic conditions: **{symptom_description}**.

Randomly generate a unique woman each time — 25 years old, hairstyle, makeup level, and facial shape, 
so every generated person looks different and realistic. 
Avoid celebrity likeness or repetition. 

Make sure the described features ({symptom_description}) are clearly visible but subtle and believable, 
as seen in a natural selfie under soft daylight. 
Do not exaggerate or distort the face — keep it natural and authentic, as if it were a real, unretouched photo.

Style: professional-quality selfie portrait, front-facing angle, clean background, balanced lighting, realistic skin texture.
"""



# url = get_image_from_model(PROMPT_IMAGE_DESC.format(target_improvement_area="lifting of drooping mouth corners and reduction of facial dynamic wrinkles"))
# print(url)

p = """
Create a natural before-and-after comparison image of the same East Asian woman showing the results of a lip augmentation procedure.
Both portraits should appear side-by-side in one image, left = before, right = after.

Subject details:
A young East Asian woman with an oval face (egg-shaped), fair and smooth skin, soft and delicate facial features, and a realistic everyday look.
Captured in a natural iPhone-style selfie angle (front-facing or slightly upward), without the phone being visible. Soft lighting, simple background, no text in the image.

Before:
Lips are naturally thin, soft makeup or no makeup, mild imperfections to maintain realism. Skin is fair but not overly airbrushed.

After:
Lip augmentation results look natural, fuller, and well-proportioned, with a gently enhanced lip contour. No exaggerated swelling. Facial expression, hairstyle, lighting, and camera angle should match the before image to ensure it is clearly the same person.

No text anywhere in the image.

"""

url = get_image_from_model(p)
print(url)



# url = get_image_from_model(PROMPT_BEFORE_DESC.format(symptom_description="mild nasolabial folds and slight skin dullness"))
# print(url)


# url = get_image_from_model(PROMPT_BEFORE_DESC.format(symptom_description="Mild double chin"))
# print(url)
