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

# 初始化
auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)

def download_images(oss_folder, local_folder, downloaded_files):
    """
    从OSS下载图片到本地文件夹
    """
    for obj in oss2.ObjectIterator(bucket, prefix=oss_folder):
        if obj.key.endswith(('.png', '.jpg', '.jpeg', '.gif')) and obj.key not in downloaded_files:
            local_file_path = os.path.join(local_folder, os.path.basename(obj.key))
            print(f"Downloading image: {obj.key}")
            bucket.get_object_to_file(obj.key, local_file_path)
            downloaded_files.add(obj.key)
            print(f"Download complete: {local_file_path}")

def create_folder_if_not_exists(folder):
    """
    如果本地文件夹不存在，则创建
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

# 路径配置
oss_folder = 'GQphoto/'
local_folder = 'C:\\Users\\Administrator\\Desktop\\watched_folder'
downloaded_files = set()

# 确保本地文件夹存在
create_folder_if_not_exists(local_folder)

# 主循环
while True:
    download_images(oss_folder, local_folder, downloaded_files)
    time.sleep(15)
