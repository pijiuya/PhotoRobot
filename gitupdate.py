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

# Initialize
auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)

# 本地配置
LOCAL_FOLDER = 'C:\\Users\\Administrator\\Desktop\\web\\download_photo'
REPO_PATH = 'C:\\Users\\Administrator\\Desktop\\web'

# 初始化OSS
auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)
oss_files = {obj.key for obj in oss2.ObjectIterator(bucket, prefix=OSS_FOLDER) if not obj.is_prefix()}

# 获取本地文件夹内容
local_files = {f for f in os.listdir(LOCAL_FOLDER) if os.path.isfile(os.path.join(LOCAL_FOLDER, f))}

# 下载新文件
new_files = oss_files - local_files
for file in new_files:
    local_filename = file.replace(OSS_FOLDER, '')
    local_file_path = os.path.join(LOCAL_FOLDER, local_filename)
    
    # 检查并创建子目录
    local_file_dir = os.path.dirname(local_file_path)
    if not os.path.exists(local_file_dir):
        os.makedirs(local_file_dir)
    
    # 下载文件
    bucket.get_object_to_file(file, local_file_path)

# Git操作
subprocess.run(['git', '-C', REPO_PATH, 'add', '.'])
subprocess.run(['git', '-C', REPO_PATH, 'commit', '-m', 'Sync new files from OSS'])
subprocess.run(['git', '-C', REPO_PATH, 'push'])