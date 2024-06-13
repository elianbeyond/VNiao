# -*- coding: utf-8 -*-
import os
import shutil
import pandas as pd

# 文件路径
excel_path = r'D:\工作\在岗\test.xlsx'
source_folder = r'D:\工作\在岗\全部金榜申报'
target_base_folder = r'D:\工作\在岗\新建文件夹'

# 读取Excel文件
df = pd.read_excel(excel_path)

# 遍历Excel每一行
for index, row in df.iterrows():
    # 确保命题编号和命题名称是字符串
    folder_suffix = str(row['命题编号'])[-3:]
    folder_name = f"{folder_suffix}-{str(row['命题名称'])}"
    target_folder = os.path.join(target_base_folder, folder_name)

    # 创建新的文件夹
    os.makedirs(target_folder, exist_ok=True)

    # 只遍历 source_folder 目录下的一级文件夹和文件
    for item in os.listdir(source_folder):
        item_path = os.path.join(source_folder, item)

        # 如果是目录，并且名称中包含命题名称，则复制整个目录
        if os.path.isdir(item_path) and str(row['命题名称']) in item:
            target_dir_path = os.path.join(target_folder, item)
            shutil.copytree(item_path, target_dir_path)

        # 如果是文件，并且名称中包含命题名称，且后缀为 .doc, .docx, .pdf，则复制文件
        elif os.path.isfile(item_path) and str(row['命题名称']) in item and (
                item.endswith('.doc') or item.endswith('.docx') or item.endswith('.pdf')):
            target_file_path = os.path.join(target_folder, item)
            shutil.copy2(item_path, target_file_path)

print("文件复制完成。")
