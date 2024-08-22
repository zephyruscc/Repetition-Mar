# 95个可打印的ASCII字符，以及一个结束符号
import string

# all_chars = set(chr(i) for i in range(32, 127))
# for i in range(32, 127):
#     print(chr(i))
#  # 去除非打印字符，如空白和控制字符
# end_symbol = "\x00"  # 非常不常见的符号，作为结束符号
#
# print(len(all_chars))
# print(all_chars)
# print(end_symbol)

# 打开并读取 train.txt 文件
with open('train.txt', 'r',encoding='utf-8') as file:
    # 逐行读取文件
    lines = file.readlines()

# 遍历每行，检查是否包含空格
passwords_with_spaces = [line.strip() for line in lines if ' ' in line]

# 输出包含空格的密码
if passwords_with_spaces:
    print("以下密码包含空格：")
    for password in passwords_with_spaces:
        print(password)
else:
    print("没有包含空格的密码。")
