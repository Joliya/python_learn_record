"""
@file: picture_size.py
@time: 2024/1/8 16:42
@desc: 
"""
import os

from PIL import Image


def resize_picture(base_pic_path, dest):
    # 获取 base_pic_path 目录下的所有文件的完整路径
    file_list = [os.path.join(base_pic_path, file_name) for file_name in os.listdir(base_pic_path)]
    for pic_path in file_list:
        if "Thumbs.db" in pic_path:
            continue
        if "DS_Store" in pic_path:
            continue
        with Image.open(pic_path) as img:

            width, height = img.size
            left = 12
            top = 0
            right = width - 12
            bottom = height

            cropped_img = img.crop((left, top, right, bottom))

            # 设置新的尺寸，比如想要缩放到200x200
            new_size = (96, 160)

            # 修改尺寸
            resized_img = cropped_img.resize(new_size)

            # 显示修改尺寸后的图片
            # resized_img.show()
            # 获取原来的图片路径中的图片名称和扩展名, 例如 /Desktop/x1.png, 得到 x1, png
            path_list = pic_path.split("/")
            path_prefix = "/".join(path_list[:-2])
            name, ext = path_list[-1].split(".")
            # 保存修改尺寸后的图片
            if not os.path.exists(f'{path_prefix}/裁剪后/{dest}'):
                os.makedirs(f'{path_prefix}/裁剪后/{dest}')
            resized_img.save(f'{path_prefix}/裁剪后/{dest}/{name}.png')


if __name__ == '__main__':
    path_list = []
    tv_name = ""
    for path in path_list:
        resize_picture(f"/Documents/互动短剧/{tv_name}/剧情树/图片/{path}", dest=path)
