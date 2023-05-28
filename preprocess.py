from PIL import Image
import os

def resize_images_in_folder(folder_path, output_size):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                # 打开图像文件
                with Image.open(file_path) as image:
                    # 调整大小并保持纵横比
                    image.thumbnail(output_size)
                    # 保存调整后的图像
                    image.save(file_path)
                    print(f"调整大小并保存图像: {filename}")
            except Exception as e:
                print(f"处理图像时出错: {filename}")
                print(str(e))

# 指定文件夹路径和输出大小
folder_path = "./tmp/"
output_size = (400, 400)

# 调整图像大小
resize_images_in_folder(folder_path, output_size)