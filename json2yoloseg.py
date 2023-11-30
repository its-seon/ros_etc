import json
import os

# Directory containing the JSON files
directory = '/home/ubuntu/segmentation_data_output'
new_directory = '/home/ubuntu/segmentation_data_output_yolo'

# Function to transform data
def transform_data(data):
    transformed = []
    for shape in data['shapes']:
        label = shape['label']
        points = shape['points']
        if label == 'track':
            label_number = '0'
        line = [label_number] + [str(coord) for point in points for coord in point]
        transformed.append(' '.join(line))
    return transformed

# Process each JSON file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        with open(os.path.join(directory, filename), 'r') as json_file:
            data = json.load(json_file)

            # Transform the data
            transformed_data = transform_data(data)

            # Write to a new TXT file
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            with open(os.path.join(new_directory, txt_filename), 'w') as txt_file:
                for line in transformed_data:
                    txt_file.write(line + '\n')

print("Conversion complete.")
