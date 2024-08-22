import string
from collections import defaultdict, Counter


class MarkovPasswordGenerator:
    def __init__(self, passwords, max_order=4, threshold=0.01):
        self.passwords = passwords
        self.max_order = max_order  # 最大的马尔可夫模型阶数
        self.threshold = threshold
        self.markov_models = [defaultdict(Counter) for _ in range(max_order)]  # 不同阶数的模型
        self.start_prob = Counter()  # 第一个字符的初始概率
        self.end_symbol = defaultdict(Counter)
        self.build_markov_models()
        self.alpha = 0.01
        self.all_chars = list(chr(i) for i in range(32, 127))  # 去除非打印字符，如空白和控制字符
        self.all_chars_end = self.all_chars.append("\x00")

    def build_markov_models(self):
        # 构建不同阶数的马尔可夫模型
        for password in self.passwords:
            password_length = len(password)

            # 统计第一个字符的频率
            if password_length > 0:
                self.start_prob[password[0]] += 1
                self.end_symbol[password_length+1] += 1   # 索引表示实际位置

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

        for order in range(1, self.max_order+1):
            for seq, transitions in self.markov_models[order].items():
                total_transitions = sum(transitions.values())
                for next_char in self.all_chars_end:
                    transition_count = transitions[next_char] + self.alpha
                    self.markov_models[order][seq][next_char] = transition_count / (total_transitions + self.alpha * 96)


    def generate_passwords(self):
        # 生成密码猜测
        passwords = []
        for start_char in self.start_prob:
            self._generate_from_node(start_char, self.start_prob[start_char], start_char, passwords, current_order=1)
        return passwords

    def _generate_from_node(self, current_seq, current_prob, current_password, passwords, current_order):
        if current_prob < self.threshold:
            return

        passwords.append(current_password)

        if current_order > self.max_order:
            return

        # 选择合适的Markov模型，根据当前序列生成下一个字符
        if current_seq not in self.markov_models[current_order - 1]:
            return

        for next_char, prob in self.markov_models[current_order - 1][current_seq].items():
            next_prob = current_prob * prob
            next_seq = (current_seq + next_char)[-current_order:]  # 更新序列，确保长度符合当前阶数
            next_order = min(current_order + 1, self.max_order)  # 动态增加阶数
            self._generate_from_node(next_seq, next_prob, current_password + next_char, passwords, next_order)


# 示例使用
passwords = ["faita18", "keila", "123456", "nash1204", "sexxi1"]

# 生成最大4阶马尔可夫模型的密码猜测
generator = MarkovPasswordGenerator(passwords, max_order=4, threshold=0.01)
generated_passwords = generator.generate_passwords()

# 输出生成的密码
print("生成的密码：")
for password in generated_passwords:
    print(password)
