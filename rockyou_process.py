# def process_file(input_file, output_file):
#     # 1. 读取文件并解析数据
#     password_list = []
#
#     with open(input_file, 'r', encoding='utf-8', errors="ignore") as file:
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
# # 示例用法
# process_file('rockyou-withcount.txt', 'processed_rockyou.txt')



import random

# 定义文件路径
input_file = "processed_rockyou.txt"
train_file = "train.txt"
test_file = "test.txt"

# 第一步：统计文件的总行数
with open(input_file, "r", encoding="utf-8") as f:  # 使用合适的编码读取文件
    lines = f.readlines()

total_lines = len(lines)
print(f"Total number of lines: {total_lines}")

# 第二步：随机选取 1e6 + 1e7 行作为候选样本
sample_size = int(1e6 + 1e7)
sample_indices = random.sample(range(total_lines), sample_size)  # 获取随机的行索引
sampled_lines = [lines[i] for i in sample_indices]

# 第三步：将前 1e6 行作为训练集
train_set = sampled_lines[:int(1e6)]

# 第四步：将剩下的 1e7 行作为测试集
test_set = sampled_lines[int(1e6):]

# 第五步：保存训练集到 train.txt
with open(train_file, "w", encoding="utf-8") as f:
    f.writelines(train_set)

# 第六步：保存测试集到 test.txt
with open(test_file, "w", encoding="utf-8") as f:
    f.writelines(sampled_lines)

print("Training and test sets have been successfully saved.")
