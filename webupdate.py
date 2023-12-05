# -*- coding: utf-8 -*-
import oss2
import time
import os
import json
import traceback
from PIL import Image

# Aliyun configuration
ACCESS_KEY_ID = 'LTAI5t8xYRR3E9hgx2STRDdw'
ACCESS_KEY_SECRET = 'XQ0Bp3VMjTVbVQojcvNmUrvHg4P7cR'
ENDPOINT = 'oss-cn-beijing.aliyuncs.com'
BUCKET_NAME = 'pjybucketname'

# Initialize
auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)

def crop_and_merge_image(original_image_path, overlay_image_path, output_image_path):
    """
    Crop and merge image with an overlay
    """
    try:
        with Image.open(original_image_path) as original:
            original_width, original_height = original.size

            # Calculate crop dimensions
            left = original_width * 0.36
            right = original_width - original_width * 0.25
            top = 0
            bottom = original_height

            # Crop the image
            cropped = original.crop((left, top, right, bottom))

            with Image.open(overlay_image_path) as overlay:
                # Resize overlay to match the cropped image
                overlay = overlay.resize(cropped.size)

                # Merge overlay onto the cropped image
                cropped.paste(overlay, (0, 0), overlay)

                # Save the processed image
                cropped.save(output_image_path)

        print(f"Image processed and saved at {output_image_path}")
    except Exception as e:
        print(f"Error processing image: {e}")
        traceback.print_exc()

def upload_files(folder_path, prefix, uploaded_files, overlay_image_path):
    """
    Upload files to OSS
    """
    print("Starting upload process")
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            local_file_path = os.path.join(folder_path, file_name)
            processed_file_path = os.path.join(folder_path, f"processed_{file_name}")
            oss_file_path = os.path.join(prefix, file_name)

            if oss_file_path not in uploaded_files:
                try:
                    print(f"Processing image: {local_file_path}")
                    crop_and_merge_image(local_file_path, overlay_image_path, processed_file_path)

                    if os.path.exists(processed_file_path):
                        print(f"Processed image exists: {processed_file_path}")

                        print(f"Uploading image: {processed_file_path}")
                        bucket.put_object_from_file(oss_file_path, processed_file_path)
                        print(f"Upload successful: {file_name}")
                    else:
                        print(f"Processed image does not exist: {processed_file_path}")

                except Exception as e:
                    print(f"Error during upload: {e}")
                    traceback.print_exc()

def get_uploaded_files(bucket, prefix):
    """
    Get list of uploaded files
    """
    print("Retrieving list of uploaded files")
    uploaded_files = []
    for obj in oss2.ObjectIterator(bucket, prefix=prefix):
        uploaded_files.append(obj.key)
    return uploaded_files

def generate_image_list_json(bucket, prefix, json_file_path):
    """
    Generate JSON file with image URLs
    """
    image_urls = []
    for obj in oss2.ObjectIterator(bucket, prefix=prefix):
        if obj.key.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_urls.append(f'https://{BUCKET_NAME}.{ENDPOINT}/{obj.key}')

    with open(json_file_path, 'w') as f:
        json.dump(image_urls, f)

# Paths
overlay_image_path = 'D:\\web\\photo_5040.png'  # Path to the overlay PNG image
local_folder = 'C:\\Users\\Administrator\\Desktop\\Place\\data\\photo'
oss_folder = 'GQrealtime/'

# Generate JSON file
json_file_path = 'D:/web/image_list.json'
generate_image_list_json(bucket, 'GQrealtime/', json_file_path)

# Main loop
while True:
    uploaded_files = get_uploaded_files(bucket, oss_folder)
    upload_files(local_folder, oss_folder, uploaded_files, overlay_image_path)
    generate_image_list_json(bucket, oss_folder, json_file_path)
    time.sleep(60)
