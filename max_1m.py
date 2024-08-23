# 定义要选取的密码数量
top_n = int(1e7)

# 定义输入和输出文件名
input_file = "generated_passwords.txt"
output_file = "top_passwords_key.txt"

# 初始化一个列表来存储密码和概率对
passwords_probabilities = []

# 读取 generated_passwords.txt 文件中的每行数据
with open(input_file, "r",encoding='utf-8') as file:
    for line in file:
        # 每行数据格式为 "密码: 概率值"，因此我们用 ':' 分隔
        try:
            password, probability = line.strip().split(": ")
            probability = float(probability)  # 转换概率值为浮点数
            passwords_probabilities.append((password, probability))
        except ValueError:
            print(f"Skipping line due to formatting issue: {line.strip()}")

# 按照概率值对列表进行排序，从高到低
passwords_probabilities.sort(key=lambda x: x[1], reverse=True)

# 选出概率最高的 top_n 个密码
top_passwords = passwords_probabilities[:top_n]

# 将这些密码写入新的文件
with open(output_file, "w",encoding='utf-8') as file:
    for password, probability in top_passwords:
        file.write(f"{password}\n")

print(f"已将概率最高的 {top_n} 个密码保存到 {output_file}")
