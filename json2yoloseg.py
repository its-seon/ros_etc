import json
import os
from PIL import Image

# Directory containing the JSON files and images
directory = '/home/ubuntu/segmentation_data_output'
image_directory = '/home/ubuntu/segmentation_data'  # 이미지 파일이 있는 디렉토리
new_directory = '/home/ubuntu/segmentation_data_output_yolo'

# Function to normalize points
def normalize_points(points, img_width, img_height):
    normalized = []
    for i, coord in enumerate(points):
        if i % 2 == 0:  # x coordinate
            normalized.append(coord / img_width)
        else:  # y coordinate
            normalized.append(coord / img_height)
    return normalized

# Function to transform data
def transform_data(data, img_size):
    transformed = []
    img_width, img_height = img_size
    for shape in data['shapes']:
        label = shape['label']
        points = shape['points']
        if label == 'track':
            label_number = '0'
        normalized_points = normalize_points([coord for point in points for coord in point], img_width, img_height)
        line = [label_number] + [str(coord) for coord in normalized_points]
        transformed.append(' '.join(line))
    return transformed

# Process each JSON file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        with open(os.path.join(directory, filename), 'r') as json_file:
            data = json.load(json_file)

            # Get image size for normalization
            img_filename = os.path.splitext(filename)[0] + '.jpg'  # Assuming image format is jpg
            with Image.open(os.path.join(image_directory, img_filename)) as img:
                img_size = img.size

            # Transform the data
            transformed_data = transform_data(data, img_size)

            # Write to a new TXT file
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            with open(os.path.join(new_directory, txt_filename), 'w') as txt_file:
                for line in transformed_data:
                    txt_file.write(line + '\n')

print("Conversion complete.")
