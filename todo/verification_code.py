import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from todo.settings import BASE_DIR

import random

# 随机字母:
def rndChar():
    return chr(random.randint(48, 57))


# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


# 240 x 60:
def get_verification_code():
    text_width = 50
    width = text_width * 4
    height = 60
    image = Image.new("RGB", (width, height), (255, 255, 255))
    # 创建Font对象:
    ttf_path = os.path.join(BASE_DIR, "assets", "ARIALN.TTF")
    font = ImageFont.truetype(ttf_path, 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 输出文字:
    string_list = []
    for t in range(4):
        char = rndChar()
        draw.text((text_width * t + 10, 10), char, font=font, fill=rndColor2())
        string_list.append(char)

    image = image.filter(ImageFilter.BLUR)
    return image, "".join(string_list)
