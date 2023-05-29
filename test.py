from PIL import Image, ImageChops, ImageEnhance
def convert_to_ela_image(path, quality):
    filename = path
    resaved_filename = filename.split('.')[0] + '.resaved.jpg'
    ELA_filename = filename.split('.')[0] + '.ela.png'

    im = Image.open(filename).convert('RGB')
    im.save(resaved_filename, 'JPEG', quality=quality)
    resaved_im = Image.open(resaved_filename)

    ela_im = ImageChops.difference(im, resaved_im)

    extrema = ela_im.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff

    ela_im = ImageEnhance.Brightness(ela_im).enhance(scale)

    return ela_im

img_out = convert_to_ela_image('./tmp/image2.png', 90)
img_out.save('./res.jpg', 'JPEG', quality = 90)

import random
from PIL import Image

import random
from PIL import Image


def random_image_manipulation(image_path):
    # 打开图像
    image = Image.open(image_path)

    # 获取图像宽度和高度
    width, height = image.size

    # 随机选择区域交换的起始点和终点
    x1 = random.randint(0, width // 2)
    y1 = random.randint(0, height // 2)
    x2 = random.randint(width // 2, width - 1)
    y2 = random.randint(height // 2, height - 1)

    # 交换图像的两个区域
    region1 = image.crop((x1, y1, x2, y2))
    region2 = image.crop((x2, y2, width, height))  # 修正此行代码
    image.paste(region2, (x1, y1, x2, y2))
    image.paste(region1, (x2, y2, width, height))  # 修正此行代码

    # 随机选择补丁的起始点和大小
    patch_size = random.randint(50, 200)
    patch_x = random.randint(0, width - patch_size)
    patch_y = random.randint(0, height - patch_size)

    # 裁剪补丁区域
    patch = image.crop((patch_x, patch_y, patch_x + patch_size, patch_y + patch_size))

    # 随机选择补丁的目标位置
    target_x = random.randint(0, width - patch_size)
    target_y = random.randint(0, height - patch_size)

    # 粘贴补丁到目标位置
    image.paste(patch, (target_x, target_y))

    # 显示和保存修改后的图像
    image.show()
    image.save("modified_image.jpg")

random_image_manipulation('./.resaved.jpg')