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

# ��������
LOCAL_FOLDER = 'C:\\Users\\Administrator\\Desktop\\web\\download_photo'
REPO_PATH = 'C:\\Users\\Administrator\\Desktop\\web'

# ��ʼ��OSS
auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)
oss_files = {obj.key for obj in oss2.ObjectIterator(bucket, prefix=OSS_FOLDER) if not obj.is_prefix()}

# ��ȡ�����ļ�������
local_files = {f for f in os.listdir(LOCAL_FOLDER) if os.path.isfile(os.path.join(LOCAL_FOLDER, f))}

# �������ļ�
new_files = oss_files - local_files
for file in new_files:
    local_filename = file.replace(OSS_FOLDER, '')
    local_file_path = os.path.join(LOCAL_FOLDER, local_filename)
    
    # ��鲢������Ŀ¼
    local_file_dir = os.path.dirname(local_file_path)
    if not os.path.exists(local_file_dir):
        os.makedirs(local_file_dir)
    
    # �����ļ�
    bucket.get_object_to_file(file, local_file_path)

# Git����
subprocess.run(['git', '-C', REPO_PATH, 'add', '.'])
subprocess.run(['git', '-C', REPO_PATH, 'commit', '-m', 'Sync new files from OSS'])
subprocess.run(['git', '-C', REPO_PATH, 'push'])