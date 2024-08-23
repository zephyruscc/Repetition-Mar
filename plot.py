import matplotlib.pyplot as plt

# 1. 读取两个文件中的数据
with open('top_passwords_key.txt', 'r', encoding='utf-8') as f:
    passwords = [line.strip() for line in f]

with open('test.txt', 'r', encoding='utf-8') as f:
    target_passwords = [line.strip() for line in f]

# 2. 初始化
cracked_passwords = []
cracked_counts = []
guess_counts = []

# 3. 逐步增加猜测数并记录破解数量
for i in range(1, len(passwords) + 1):
    # 当前猜测的密码
    guess_password = passwords[i - 1]

    # 统计 guess_password 在 target_passwords 中出现的次数
    match_count = target_passwords.count(guess_password)

    # 如果该密码在目标集合中出现
    if match_count > 0:
        cracked_passwords.extend([guess_password] * match_count)  # 添加所有匹配的密码
        target_passwords = [pwd for pwd in target_passwords if pwd != guess_password]  # 移除所有已破解的密码

    # 每隔一定数量记录一次破解情况 (比如每1000次猜测记录一次)
    if i % 100000 == 0 or i == len(passwords):
        print(i)
        guess_counts.append(i)
        cracked_counts.append(len(cracked_passwords))

# 保存 guess_counts 到 guess_counts.txt
with open('guess_counts4.txt', 'w', encoding='utf-8') as f:
    for item in guess_counts:
        f.write(f"{item}\n")

# 保存 cracked_counts 到 cracked_counts.txt
with open('cracked_counts4.txt', 'w', encoding='utf-8') as f:
    for item in cracked_counts:
        f.write(f"{item}\n")

# 保存 target_passwords 到 target_passwords.txt
with open('target_passwords4.txt', 'w', encoding='utf-8') as f:
    for item in target_passwords:
        f.write(f"{item}\n")

# 4. 绘制破解数随猜测数变化的折线图
# plt.plot(guess_counts, cracked_counts, marker='o')
# plt.title('Number of Passwords Cracked vs. Number of Guesses')
# plt.xlabel('Number of Guesses')
# plt.ylabel('Number of Passwords Cracked')
# plt.grid(True)
# # 设置横坐标范围为 0 到 3e8
# plt.xlim(0, 3e8)
# plt.show()