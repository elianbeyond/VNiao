# -*- coding: utf-8 -*-
import os

# 根目录
root_folder = r'D:\工作\在岗\全部金榜申报附件整理'

# 用于存储空文件夹的列表
empty_folders = []

# 遍历根目录下的所有文件夹
for root, dirs, files in os.walk(root_folder):
    for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)

        # 检查文件夹是否为空
        if not os.listdir(dir_path):
            empty_folders.append(dir_path)

# 打印空文件夹的名字和总数
print("空文件夹列表：")
for folder in empty_folders:
    print(folder)

print(f"总共有 {len(empty_folders)} 个空文件夹。")
