import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud


class MyWordCloud:
    def __init__(self):
        self.FILE_PATH = ''
        self.FILE_NAME = ''
        self.FONT_NAME = "./NanumSquareB.ttf"

        self.width = 1200
        self.height = 800
        self.background_color = 'white'
        self.color_func = None
        self.is_font_size_norm = False

    def set_init(self, width, height, background_color, word_color, is_font_size_norm):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.color_func = None
        self.is_font_size_norm = is_font_size_norm

    def _similar_color_func(self, word=None, font_size=None, position=None, orientation=None,
                            font_path=None, random_state=None):
        h = 40  # 색상, 0 - 360
        s = 100  # 채도, 0 - 100
        l = random_state.randint(30, 70)  # 명도, 0 - 100
        return "hsl({}, {}%, {}%)".format(h, s, l)

    def _multi_color_func(self, word=None, font_size=None, position=None, orientation=None,
                          font_path=None, random_state=None):
        colors = [[4, 87, 72],
                  [25, 84, 75],
                  [82, 53, 74],
                  [158, 58, 69]]
        rand = random_state.randint(0, len(colors) - 1)
        return "hsl({}, {}%, {}%)".format(colors[rand][0], colors[rand][1], colors[rand][2])

    def _draw_word_cloud(self, word2cnt):
        word_cloud = WordCloud(font_path=self.FONT_NAME,
                               width=self.width, height=self.height,
                               background_color=self.background_color,
                               color_func=self.color_func)
        word_cloud = word_cloud.generate_from_frequencies(word2cnt)
        plt.figure(figsize=(12, 8))
        plt.imshow(word_cloud)
        plt.axis('off')
        plt.show()

    def count_word(self, data):
        word2cnt = {}
        for word in data:
            if word not in word2cnt.keys():
                word2cnt[word] = 1
            else:
                word2cnt[word] += 1
        return word2cnt

    def normalize_input_data(self, data):
        if type(data) == dict:
            word2cnt = data
        elif type(data) == list:
            word2cnt = self.count_word(data)
        elif type(data[0]) == list:
            temp = []
            for words in data:
                temp += words
            word2cnt = self.count_word(temp)
        else:
            print('Input type error (Input type : list[[str]] or list[] or str')
            raise ValueError

        return word2cnt

    def normalize_data(self, data):
        max_val = max(data.values())
        min_val = min(data.values())

        for k, v in data.items():
            data[k] = (v - min_val + 1) / (max_val - min_val + 1) * 100

        return data

    def set_color_func(self, word_color):
        if word_color == 'similar':
            self.color_func = self._similar_color_func
        elif word_color == 'multi':
            self.color_func = self._multi_color_func
        else:
            self.color_func = None

    def draw_word_cloud(self, data, width=1200, height=800, background_color='white',
                        word_color="standard", is_font_size_norm=False):
        # 기본값 세팅
        self.set_init(width=width, height=height, background_color=background_color,
                      word_color=word_color, is_font_size_norm=is_font_size_norm)

        # 워드클라우드 글자색 선택 (standard or similar or multi)
        self.set_color_func(word_color)

        # 입력 데이터 정규화 (list or list[list] or dict -> dict)
        word2cnt = self.normalize_input_data(data)

        # 워드클라우드 출력
        self._draw_word_cloud(word2cnt)


if __name__ == '__main__':
    # corpus = [['dog', 'dog', 'cat', 'dog', 'cow', 'cat', 'tiger'], ['dog', 'dog', 'cat'], ['cow']]
    dic = {'dog': 10, 'cat': 6, 'horse': 5, 'cow': 4, 'rabbit': 7, 'tiger': 2}
    mwc = MyWordCloud()
    mwc.draw_word_cloud(dic, word_color='multi')
