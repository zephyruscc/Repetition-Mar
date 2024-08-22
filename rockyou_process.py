# def process_file(input_file, output_file):
#     # 1. 读取文件并解析数据
#     password_list = []
#
#     with open(input_file, 'r', encoding='utf-8') as file:
#         for line in file:
#             parts = line.strip().split(maxsplit=1)
#             if len(parts) == 2:
#                 try:
#                     count = int(parts[0])  # 出现次数
#                     password = parts[1]  # 密码
#                     # 根据出现次数重复密码并添加到列表
#                     password_list.extend([password] * count)
#                 except ValueError:
#                     # 如果出现次数不是整数，跳过这一行
#                     continue
#
#     # 2. 将处理后的密码写入新文件
#     with open(output_file, 'w', encoding='utf-8') as file:
#         for password in password_list:
#             file.write(f"{password}\n")
#
#
# # 示例用法
# process_file('myspace-withcount.txt', 'processed_myspace.txt')


import random


def split_file(input_file, output_file1, output_file2):
    # 1. 读取文件
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 2. 打乱行顺序
    random.shuffle(lines)

    # 3. 计算分割点
    mid_point = len(lines) // 2

    # 4. 分割数据
    part1 = lines[:mid_point]
    part2 = lines[mid_point:]

    # 5. 保存到新文件
    with open(output_file1, 'w', encoding='utf-8') as file1:
        file1.writelines(part1)

    with open(output_file2, 'w', encoding='utf-8') as file2:
        file2.writelines(part2)


# 示例用法
split_file('processed_myspace.txt', 'myspace_train.txt', 'myspace_test.txt')