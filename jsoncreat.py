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
    folder_to_watch = 'C:\\Users\\Administrator\\Desktop\\web\\download_photo' # 更改为您的图片文件夹路径
    output_json = 'C:\\Users\\Administrator\\Desktop\\web\\image_list.json' # 输出JSON文件的路径

    while True:
        generate_image_list_json(folder_to_watch, output_json)
        time.sleep(60) # 每60秒运行一次

if __name__ == "__main__":
    main()
