# 95个可打印的ASCII字符，以及一个结束符号
import string

# all_chars = list(chr(i) for i in range(32, 127))
# for i in range(32, 127):
#     print(chr(i))
#  # 去除非打印字符，如空白和控制字符
# end_symbol = "\x00"  # 非常不常见的符号，作为结束符号
#
# print(len(all_chars))
# print(all_chars)
# print(end_symbol)

# # 打开并读取 train.txt 文件
# with open('train.txt', 'r',encoding='utf-8') as file:
#     # 逐行读取文件
#     lines = file.readlines()
#
# # 遍历每行，检查是否包含空格
# passwords_with_spaces = [line.strip() for line in lines if ' ' in line]
#
# # 输出包含空格的密码
# if passwords_with_spaces:
#     print("以下密码包含空格：")
#     for password in passwords_with_spaces:
#         print(password)
# else:
#     print("没有包含空格的密码。")
from collections import defaultdict, Counter

class MarkovPasswordGenerator:
    def __init__(self, passwords, max_order=4, threshold=0.01):
        self.passwords = passwords
        self.max_order = max_order  # 最大的马尔可夫模型阶数
        self.threshold = threshold
        self.markov_models = {order: defaultdict(Counter) for order in range(1, max_order + 1)}
        self.start_prob = Counter()  # 第一个字符的初始概率
        self.alpha = 0.01
        self.all_chars = list(chr(i) for i in range(32, 127))  # 去除非打印字符，如空白和控制字符
        self.all_chars_end = list(chr(i) for i in range(32, 127)) + ['\x00']
        self.build_markov_models()

    def build_markov_models(self):
        # 构建不同阶数的马尔可夫模型
        for password in self.passwords:
            password_length = len(password)

            # 统计第一个字符的频率
            if password_length > 0:
                self.start_prob[password[0]] += 1

            # 低阶位置
            for order in range(1, self.max_order):
                if password_length < order:
                    continue
                sequence = password[0:order]

                if password_length == order:
                    self.markov_models[order][sequence]["\x00"] += 1
                    continue

                next_char = password[order]
                self.markov_models[order][sequence][next_char] += 1

            # 高阶位置
            if password_length == self.max_order:
                self.markov_models[self.max_order][password]["\x00"] += 1

            if password_length > self.max_order:
                for i in range(password_length - order):
                    sequence = password[i:i + order]
                    next_char = password[i + order]
                    self.markov_models[self.max_order][sequence][next_char] += 1
                end_sequence = password[-self.max_order:]
                self.markov_models[self.max_order][end_sequence]["\x00"] += 1

        # 将计数转换为概率
        total_starts = sum(self.start_prob.values())
        for char in self.all_chars:
            self.start_prob[char] = (self.start_prob[char] + self.alpha) / (total_starts + self.alpha * 95)

        for order in range(1, self.max_order + 1):
            for seq, transitions in self.markov_models[order].items():
                total_transitions = sum(transitions.values())
                for next_char in self.all_chars_end:
                    transition_count = transitions[next_char] + self.alpha
                    self.markov_models[order][seq][next_char] = transition_count / (total_transitions + self.alpha * 96)


passwords = ["faita18", "keila", "123456", "nash1204", "sexxi1"]

# 生成最大4阶马尔可夫模型的密码猜测
generator = MarkovPasswordGenerator(passwords, max_order=4, threshold=0.01)
print(generator.markov_models)
print(generator.start_prob)
for start_char in generator.start_prob:
    print(generator.start_prob[start_char])



# import pandas as pd
#
# def display_markov_model_as_table(markov_models):
#     # 创建一个空的 DataFrame
#     data = []
#
#     # 遍历每个阶数的 Markov 模型
#     for order, transitions in markov_models.items():
#         for seq, next_chars in transitions.items():
#             for next_char, prob in next_chars.items():
#                 # 将每个序列及其对应的下一个字符和概率添加到数据中
#                 data.append([order, seq, next_char, prob])
#
#     # 将数据转换为 DataFrame
#     df = pd.DataFrame(data, columns=["Order", "Sequence", "Next Char", "Probability"])
#
#     # 打印表格
#     print(df)
#
#     df.to_csv("markov_model.csv", index=False, encoding="utf-8")
#     print(f"Markov model saved to {"markov_model.csv"}")
#
# # 使用示例
# display_markov_model_as_table(generator.markov_models)