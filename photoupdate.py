# -*- coding: utf-8 -*-
import oss2
import time
import os
import json

# Aliyun configuration
ACCESS_KEY_ID = 'LTAI5t8xYRR3E9hgx2STRDdw'
ACCESS_KEY_SECRET = 'XQ0Bp3VMjTVbVQojcvNmUrvHg4P7cR'
ENDPOINT = 'oss-cn-beijing.aliyuncs.com'
BUCKET_NAME = 'pjybucketname'

# Initialize
auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)

def upload_files(folder_path, prefix, uploaded_files):
    """
    Upload files to OSS
    """
    print("Starting upload process")
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            local_file_path = os.path.join(folder_path, file_name)
            oss_file_path = os.path.join(prefix, file_name)

            if oss_file_path not in uploaded_files:
                try:
                    print(f"Uploading image: {local_file_path}")
                    bucket.put_object_from_file(oss_file_path, local_file_path)
                    print(f"Upload successful: {file_name}")
                except Exception as e:
                    print(f"Error during upload: {e}")

def get_uploaded_files(bucket, prefix):
    """
    Get list of uploaded files
    """
    print("Retrieving list of uploaded files")
    uploaded_files = []
    for obj in oss2.ObjectIterator(bucket, prefix=prefix):
        uploaded_files.append(obj.key)
    return uploaded_files

# Paths
local_folder = 'C:\\Users\\Administrator\\Desktop\\Place\\data\\photo'
oss_folder = 'GQphoto/'

# Main loop
while True:
    uploaded_files = get_uploaded_files(bucket, oss_folder)
    upload_files(local_folder, oss_folder, uploaded_files)
    time.sleep(60)