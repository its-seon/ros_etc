import os
from PIL import Image

def get_image_sizes(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            img_path = os.path.join(directory, filename)
            with Image.open(img_path) as img:
                print(f"{filename}: {img.size}")

directory = '/home/ubuntu/yolov8_seg/kiro_track/images'  # 여기에 이미지가 있는 디렉토리 경로를 입력하세요.
get_image_sizes(directory)
