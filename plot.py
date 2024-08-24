import matplotlib.pyplot as plt

# 1. 读取两个文件中的数据
with open('top_passwords_key5.txt', 'r', encoding='utf-8') as f:
    passwords = [line.strip() for line in f]

with open('output2.txt', 'r', encoding='utf-8') as f:
    target_passwords = {}
    for line in f:
        # 按照 '：' 分割每行数据，前者为密码，后者为出现次数
        key, value = line.strip().split('：')
        target_passwords[key.strip()] = int(value.strip())

# 2. 初始化变量
total_count = 0
count = 0
stored_results = []
guess_number = []

# 3. 遍历密码并统计
for password in passwords:
    if password in target_passwords.keys():
        total_count += target_passwords[password]

    count += 1

    if count % 1000 == 0:
        print(count)

    # 每统计100000个密码后，存储结果
    if count % 100000 == 0 or count == len(passwords):
        stored_results.append(total_count)
        guess_number.append(count)

# 5. 将存储的数组写入到本地txt文件
with open('stored_results55.txt', 'w', encoding='utf-8') as f:
    for result in stored_results:
        f.write(f"{result}\n")

with open('guess_number55.txt', 'w', encoding='utf-8') as f:
    for result in guess_number:
        f.write(f"{result}\n")

print("存储结果已保存到 stored_results.txt 文件中。")

# 4. 绘制破解数随猜测数变化的折线图
# plt.plot(guess_counts, cracked_counts, marker='o')
# plt.title('Number of Passwords Cracked vs. Number of Guesses')
# plt.xlabel('Number of Guesses')
# plt.ylabel('Number of Passwords Cracked')
# plt.grid(True)
# # 设置横坐标范围为 0 到 3e8
# plt.xlim(0, 3e8)
# plt.show()