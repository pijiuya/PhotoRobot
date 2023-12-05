# -*- coding: utf-8 -*-
import os
import json
import time

def generate_image_list_json(directory, output_file):
    """creat"""
    images = [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    with open(output_file, 'w') as f:
        json.dump(images, f)

def main():
    folder_to_watch = 'C:\\Users\\Administrator\\Desktop\\web\\download_photo' # ����Ϊ����ͼƬ�ļ���·��
    output_json = 'C:\\Users\\Administrator\\Desktop\\web\\image_list.json' # ���JSON�ļ���·��

    while True:
        generate_image_list_json(folder_to_watch, output_json)
        time.sleep(60) # ÿ60������һ��

if __name__ == "__main__":
    main()
