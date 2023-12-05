# -*- coding: utf-8 -*-
import oss2
import os
import subprocess

# Aliyun configuration
ACCESS_KEY_ID = 'LTAI5t8xYRR3E9hgx2STRDdw'
ACCESS_KEY_SECRET = 'XQ0Bp3VMjTVbVQojcvNmUrvHg4P7cR'
ENDPOINT = 'oss-cn-beijing.aliyuncs.com'
BUCKET_NAME = 'pjybucketname'
OSS_FOLDER = 'GQrealtime/'

# Initialize OSS
auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)

# Local configuration
LOCAL_FOLDER = 'C:\\Users\\Administrator\\Desktop\\web\\download_photo'
REPO_PATH = 'C:\\Users\\Administrator\\Desktop\\web'

# Fetching OSS folder contents
# Fetching OSS folder contents
print("Fetching OSS folder contents...")
oss_files = {obj.key[len(OSS_FOLDER):] for obj in oss2.ObjectIterator(bucket, prefix=OSS_FOLDER) if obj.key[-1] != '/'}

# Fetching local folder contents
print("Fetching local folder contents...")
local_files = {f for f in os.listdir(LOCAL_FOLDER) if os.path.isfile(os.path.join(LOCAL_FOLDER, f))}

# Download new files
for file in oss_files:
    if file not in local_files:
        local_file_path = os.path.join(LOCAL_FOLDER, file)

        # Ensure local file directory exists
        local_file_dir = os.path.dirname(local_file_path)
        if not os.path.exists(local_file_dir):
            os.makedirs(local_file_dir)

        # Download file
        print(f"Downloading {file} to {local_file_path}")
        bucket.get_object_to_file(OSS_FOLDER + file, local_file_path)

# Git operations
print("Running Git operations...")
subprocess.run(['git', '-C', REPO_PATH, 'add', '.'])
subprocess.run(['git', '-C', REPO_PATH, 'commit', '-m', 'Sync new files from OSS'])
subprocess.run(['git', '-C', REPO_PATH, 'push'])
