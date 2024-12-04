import os
import subprocess
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ####### util # #######
def get_subdirectories(directory):
    # 获取指定目录下所有的文件和文件夹
    all_files = os.listdir(directory)

    # 过滤出所有的文件夹
    subdirectories = [f for f in all_files if os.path.isdir(os.path.join(directory, f))]

    return subdirectories


def get_files_in_directory(directory):
    # 获取指定目录下所有的文件和文件夹
    all_files = os.listdir(directory)

    # 过滤出所有的文件
    files = [f for f in all_files if os.path.isfile(os.path.join(directory, f))]

    return files


def display_image(image):
    """
    显示生成的图像

    参数：
    image (numpy.ndarray): 生成的图像
    """
    plt.imshow(image, cmap='gray', interpolation='nearest')
    plt.title("Generated Image from Data")
    plt.axis('off')
    plt.show()


def to_burst_sequence(packet_sequence, target_length):
    burst_sequence = []
    current_direction = 0
    count = 0

    for packet in packet_sequence:
        if packet == current_direction:
            count += 1
        else:
            if current_direction != 0 and count > 0:
                # 对突发包数量进行符号化处理，-1方向用负值表示
                burst_sequence.append(count if current_direction == 1 else -count)
            current_direction = packet
            count = 1

    # 处理最后一段突发包
    if current_direction != 0 and count > 0:
        burst_sequence.append(count if current_direction == 1 else -count)

    original_length = len(burst_sequence)
    # 填充或截断突发包序列
    if len(burst_sequence) < target_length:
        # 填充0
        burst_sequence.extend([0] * (target_length - len(burst_sequence)))
    elif len(burst_sequence) > target_length:
        # 截断序列
        burst_sequence = burst_sequence[:target_length]

    return burst_sequence, original_length


def array_to_image(arr, height=1024, width=1088, scale=17):
    # 创建一个全零的空白图像（高度×宽度，RGBA四通道）
    image = np.zeros((height, width, 4), dtype=np.uint8)
    image[:] = [0, 0, 255, 255]

    # 遍历数组，填充每一行
    for i in range(height):  # 高度为1024，按行填充
        value = arr[i]  # 当前行的值
        if value > 0:
            color = [255, 0, 0, 255]  # 红色 + 不透明度
        elif value < 0:
            color = [0, 255, 0, 255]  # 绿色 + 不透明度
        else:
            color = [0, 0, 255, 255]  # 蓝色 + 不透明度

        # 计算该行的颜色块数，确保不会超出宽度1024
        num_blocks = min(abs(value) * scale, width)

        # 填充颜色块（确保每行不超过1024像素）
        image[i, :num_blocks] = color

    # 确保图像数据类型为uint8，防止超出范围
    image = np.clip(image, 0, 255).astype(np.uint8)

    # 转换为PIL图像并保存为PNG格式
    img = Image.fromarray(image, 'RGBA')
    return img


def split_npz_by_label(file_path, output_dir):
    """
    按照 npz 文件中的标签 (label) 将数据划分，并保存到以标签命名的文件夹中。

    参数：
        file_path (str): 输入的 .npz 文件路径。
        output_dir (str): 输出目录，用于保存划分后的文件。
    """
    # 加载 .npz 文件
    data = np.load(file_path, allow_pickle=True)

    # 获取数据和标签
    data_array = data['data']
    labels_array = data['labels']

    # 获取唯一的标签
    unique_labels = np.unique(labels_array)

    # 按照标签划分数据并保存
    for label in unique_labels:
        # 将域名中的 . 替换为 -
        safe_label = label.replace('.', '-')

        # 筛选出当前标签的数据
        label_mask = labels_array == label
        label_data = data_array[label_mask]

        # 创建以 safe_label 为名的文件夹
        label_output_dir = os.path.join(output_dir, f"{safe_label}")
        os.makedirs(label_output_dir, exist_ok=True)

        # 将每条数据单独保存为 safe_label_i.npz
        for i, data_entry in enumerate(label_data):
            output_file_path = os.path.join(label_output_dir, f"{safe_label}_{i}.npz")
            np.savez(output_file_path, data=data_entry, label=label)

        print(f"Saved {len(label_data)} files for label {label} in folder {label_output_dir}")


def trans_website_to_png(npz_file_dir, output_dir):
    # 找到文件
    directory_path = npz_file_dir
    files = get_files_in_directory(directory_path)

    p = 0
    # 创建输出文件夹
    os.makedirs(output_dir, exist_ok=True)
    for index, file in enumerate(files):
        # 加载 .npz 文件
        data = np.load(directory_path + '/' + file, allow_pickle=True)
        # 获取数据和标签
        data_array = data['data']
        data_burst, original_len = to_burst_sequence(data_array, 1024)
        if original_len > p:
            p = original_len
        # label_array = data['label']
        # 创建图像
        img = array_to_image(data_burst)
        filename = file.replace('.npz', '.png')
        # 显示图像
        img.save(output_dir + '/' + filename)

    return p


def trans_npz_to_png(npz_file_dir):
    # 获取所有网站
    directory_path = npz_file_dir
    subdirectories = get_subdirectories(directory_path)
    p = 0
    # 为将每个网站的NPZ数据转成png
    for subdirectory in subdirectories:
        print("Translating " + subdirectory + " to png")
        max_burst_len = trans_website_to_png(directory_path + '/' + subdirectory,
                                             directory_path + '_jpg/' + subdirectory)
        if max_burst_len > p:
            p = max_burst_len
    return p


if __name__ == '__main__':
    # Step1 将不同的website流数据分成子文件
    # file_path = '../data/npzdata/CW/tor_100w_2500tr.npz'
    # output_dir = '../data/npzdata/CW/tor_100w_2500tr'
    # split_npz_by_label(file_path, output_dir)

    # step2 将子文件转成png
    max_burst_len = trans_npz_to_png('../data/npzdata/CW/tor_100w_2500tr')
    print(max_burst_len)
