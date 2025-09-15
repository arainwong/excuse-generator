import random
import csv
from collections import defaultdict

class ExcuseGenerator:
    def __init__(self, csv_path=None, seed=None):
        """
        neutral decorations -> person & object
        """
        if seed is not None:
            random.seed(seed)
        
        self.positive_prob = 0.22
        self.neutral_prob = 0.25

        self.person_prob = 0.4
        self.object_prob = 0.3

        self.excuse_dict = defaultdict(list)

        if csv_path:
            self.load_csv(csv_path)
        else:
            # if no csv then use default dict
            self.excuse_dict["special"] = [
                "声音听不清","手柄有延迟","手柄漂移","游戏掉帧",
                "我太困了","我太累了","手机响了","猫跳键盘了","网络太卡",
                "椅子太硬了","桌子太晃了","耳机坏了","屏幕看不清","太累反应有点慢了",
                ]
            
            self.excuse_dict["positive_person_nouns"] = ["对面"]
            self.excuse_dict["positive_person_decorations"] = [
                "有点厉害","运气真好","真阴","有小代","有点准","真能苟","真卡",
                ]
            
            self.excuse_dict["positive_object_nouns"] = ["对面武器","对面配合",]
            self.excuse_dict["positive_object_decorations"] = ["真恶心",]

            self.excuse_dict["positive_neutral_decorations"] = ["真恶心"]

            self.excuse_dict["negative_person_nouns"] = ["队友"]
            self.excuse_dict["negative_person_decorations"] = [
                "太弱","在干嘛？","跟不上","没意识","太慢","太烂","太猥琐",
                "真能送","乱跑","瞎打","不敢冲","菜逼","漏人了","啥比啊"
                ]
            
            self.excuse_dict["negative_object_nouns"] = [
                "网络","我们配合","灵敏度","游戏","地图","手感","乱数","武器平衡",
                ]
            self.excuse_dict["negative_object_decorations"] = [
                "太差","有问题","不好","不行","有点离谱"
                ]
            
            self.excuse_dict["negative_neutral_decorations"] = ["真恶心","真垃圾",]

    def load_csv(self, path):
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            reader.fieldnames = [name.strip() for name in reader.fieldnames]
            for row in reader:
                cat = row["category"].strip()
                word = row["word"].strip()
                if cat and word:
                    self.excuse_dict[cat].append(word)


    def make_special(self) -> str:
        return [f"special " ,random.choice(self.excuse_dict["special"])]

    def make_person_excuse(self) -> str:
        noun_prob = random.random() # return random a number (0, 1)
        word_prob = random.random()
        cat = []
        if noun_prob < self.positive_prob:
            noun = random.choice(self.excuse_dict["positive_person_nouns"])
            if word_prob < self.neutral_prob:
                word = random.choice(self.excuse_dict["positive_neutral_decorations"])
            else:
                word = random.choice(self.excuse_dict["positive_person_decorations"])
            cat.append('positive')
        else:
            noun = random.choice(self.excuse_dict["negative_person_nouns"])
            if word_prob < self.neutral_prob:
                word = random.choice(self.excuse_dict["negative_neutral_decorations"])
            else:
                word = random.choice(self.excuse_dict["negative_person_decorations"])
            cat.append('negative')
        
        s = ''.join(cat)
        return [s, f"{noun}{word}"]

    def make_object_excuse(self) -> str:
        noun_prob = random.random()
        word_prob = random.random()
        cat = []
        if noun_prob < self.positive_prob:
            noun = random.choice(self.excuse_dict["positive_object_nouns"])
            if word_prob < self.neutral_prob:
                word = random.choice(self.excuse_dict["positive_neutral_decorations"])
            else:
                word = random.choice(self.excuse_dict["positive_object_decorations"])
            cat.append('positive')
        else:
            noun = random.choice(self.excuse_dict["negative_object_nouns"])
            if word_prob < self.neutral_prob:
                word = random.choice(self.excuse_dict["negative_neutral_decorations"])
            else:
                word = random.choice(self.excuse_dict["negative_object_decorations"])
            cat.append('negative')
        
        s = ''.join(cat)
        return [s, f"{noun}{word}"]

    def generate(self) -> str:
        cat_prob = random.random()
        if cat_prob < self.person_prob:
            result = self.make_person_excuse()
        elif cat_prob < self.person_prob + self.object_prob:
            result = self.make_object_excuse()
        else:
            result = self.make_special()
        return result


if __name__ == "__main__":
    g = ExcuseGenerator(csv_path="config/excuse_dictionary.csv")
    # print(g.excuse_dict)
    num_samples = 100
    special_counter = 0
    pos_counter = 0
    neg_counter = 0
    for s in range(num_samples):
        cat, sample = g.generate()
        if cat == 'special':
            special_counter += 1
        elif cat == 'positive':
            pos_counter += 1
        elif cat == 'negative':
            neg_counter += 1
        print(cat, sample)
    print(f'special counter: {(special_counter/num_samples):.2f}, theoritical: {(1-g.person_prob-g.object_prob):.2f}')
    print(f'positive counter: {(pos_counter/num_samples):.2f}, theoritical: {(g.person_prob*g.positive_prob):.2f}+{(g.object_prob*g.positive_prob):.2f}={(g.person_prob*g.positive_prob+g.object_prob*g.positive_prob):.2f}')
    print(f'negative counter: {(neg_counter/num_samples):.2f}, theoritical: {(g.person_prob*(1-g.positive_prob)):.2f}+{(g.object_prob*(1-g.positive_prob)):.2f}={(g.person_prob*(1-g.positive_prob)+g.object_prob*(1-g.positive_prob)):.2f}')

