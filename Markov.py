from collections import defaultdict, Counter

class MarkovPasswordGenerator:
    def __init__(self, passwords, max_order=4, threshold=0.01):
        self.passwords = passwords
        self.max_order = max_order  # 马尔可夫模型阶数
        self.threshold = threshold
        self.markov_models = {order: defaultdict(Counter) for order in range(1, max_order + 1)}
        self.start_prob = Counter()  # 第一个字符的初始概率
        self.alpha = 0.01
        self.all_chars = list(chr(i) for i in range(32, 127))  # 95个字符
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
                for i in range(password_length - self.max_order):
                    sequence = password[i:i + self.max_order]
                    next_char = password[i + self.max_order]
                    self.markov_models[self.max_order][sequence][next_char] += 1
                end_sequence = password[-self.max_order:]
                self.markov_models[self.max_order][end_sequence]["\x00"] += 1

        # 将计数转换为概率
        total_starts = sum(self.start_prob.values())

        for char, value in self.start_prob.items():
            self.start_prob[char] = (self.start_prob[char] + self.alpha) / (total_starts + self.alpha * 95)

        for order in range(1, self.max_order + 1):
            for seq, transitions in self.markov_models[order].items():
                total_transitions = sum(transitions.values())
                for next_char in self.all_chars_end:
                    transition_count = transitions[next_char] + self.alpha
                    self.markov_models[order][seq][next_char] = transition_count / (total_transitions + self.alpha * 96)


    def generate_passwords(self):
        # 生成密码猜测
        passwords = {}
        for start_char in self.start_prob:
            dic = self._generate_from_node(start_char, self.start_prob[start_char])
            passwords.update(dic)
        print(len(passwords))
        return passwords

    def _generate_from_node(self, start_char, start_pr):
        if start_pr < self.threshold:
            return {}
        password_end = {}

        password_dic = {start_char:start_pr}

        while password_dic:
            # 迭代新的密码
            new_password_dic = {}
            for i in password_dic.keys():
                password_length = len(i)

                # 低阶密码处理
                for order in range(1, self.max_order):
                    if password_length == order:

                        for chr1 in self.all_chars:
                            next_pr = password_dic[i] * self.markov_models[order][i][chr1]
                            if next_pr > self.threshold:
                                new_password_dic[i+chr1]= next_pr

                        end_pr = password_dic[i] * self.markov_models[order][i]["\x00"]
                        if end_pr >= self.threshold:
                             password_end[i] = end_pr

                # 高阶位置
                if password_length >= self.max_order:
                    sequence = i[-self.max_order:]

                    for chr1 in self.all_chars:
                        next_pr = password_dic[i] * self.markov_models[self.max_order][sequence][chr1]
                        if next_pr > self.threshold:
                            new_password_dic[i+chr1] = next_pr

                    end_pr = password_dic[i] * self.markov_models[self.max_order][sequence]["\x00"]
                    if end_pr >= self.threshold:
                        password_end[i] = end_pr

            password_dic = new_password_dic

        return password_end

# 读取训练集
passwords = []
# 读取 train.txt 文件中的每行内容并存储到数组中
with open("train.txt", "r",encoding='utf-8') as file:
    passwords = [line.strip() for line in file]

# 生成 n 阶马尔可夫模型的密码猜测
# 生成密码数 概率阈值 order
# 34886259 1e-9 3
# 14237751 1e-9 5
generator = MarkovPasswordGenerator(passwords, max_order=5, threshold=1e-9)
generated_passwords = generator.generate_passwords()

# 将字典保存到本地 txt 文件
with open("generated_passwords5_onemar.txt", "w",encoding='utf-8') as txt_file:
    for key, value in generated_passwords.items():
        txt_file.write(f"{key}: {value}\n")

print("字典已保存为 generated_passwords.txt")