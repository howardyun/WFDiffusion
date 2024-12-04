import os
import sys

import os

import os

def delete_txt_files(data_dir):
    """
    遍历指定目录下的每个子文件夹，删除其中的所有 .txt 文件。

    :param data_dir: 数据目录的路径，包含子文件夹和文件。
    """
    for website in os.listdir(data_dir):
        # 获取每个子文件夹的路径
        website_dir = os.path.join(data_dir, website)

        # 确保是一个目录
        if not os.path.isdir(website_dir):
            continue

        # 遍历子文件夹中的文件
        for filename in os.listdir(website_dir):
            # 获取文件的完整路径
            file_path = os.path.join(website_dir, filename)

            # 如果是 .txt 文件，则删除
            if filename.endswith('.txt'):
                os.remove(file_path)
                print(f'Deleted {file_path}')


# 示例调用




def create_txt_files(data_dir, content_template='pixelated network data, type is {website}'):
    """
    遍历指定目录下的每个子文件夹，为每个文件创建一个同名的 .txt 文件并写入内容。

    :param data_dir: 数据目录的路径，包含子文件夹和文件。
    :param content_template: 要写入文本文件的内容模板，支持格式化。
    """
    for website in os.listdir(data_dir):
        # 获取每个子文件夹的路径
        website_dir = os.path.join(data_dir, website)

        # 确保是一个目录
        if not os.path.isdir(website_dir):
            continue

        # 遍历子文件夹中的文件
        for filename in os.listdir(website_dir):
            # 获取文件的完整路径
            file_path = os.path.join(website_dir, filename)

            # 获取不带扩展名的文件名
            base_filename = os.path.splitext(filename)[0]

            # 创建同名的txt文件，路径为 website_dir/base_filename.txt
            txt_file_path = os.path.join(website_dir, f'{base_filename}.txt')

            # 打开文件并写入内容
            with open(txt_file_path, 'w') as f:
                # 格式化并写入内容
                content = content_template.format(website=website)
                f.write(content)
            print(f'Created {txt_file_path} and wrote content: {content}')



# 创建txt
create_txt_files('../data/npzdata/CW/tor_100w_2500tr_jpg')

# 删除txt
# delete_txt_files('../data/npzdata/CW/tor_100w_2500tr_jpg')






