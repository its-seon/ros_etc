import os
import shutil

source_dir = '/home/ubuntu/segmentation_data_output_yolo'  # .txt 파일이 있는 디렉토리
target_dir = '/home/ubuntu/segmentation_data'  # 파일을 찾을 디렉토리
destination_dir = '/home/ubuntu/yolov8_seg/kiro_track/images'  # 파일을 복사할 디렉토리

# source_dir에서 .txt 파일의 이름 찾기
source_filenames = {os.path.splitext(filename)[0] for filename in os.listdir(source_dir) if filename.endswith('.txt')}

# target_dir에서 동일한 이름을 가진 파일 찾기 및 복사
for target_file in os.listdir(target_dir):
    basename = os.path.splitext(target_file)[0]
    if basename in source_filenames:
        # 파일을 destination_dir로 복사
        shutil.copy(os.path.join(target_dir, target_file), destination_dir)

print("File copying complete.")
