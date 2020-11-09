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
        self.word_color = 'standard'
        self.is_font_size_norm = False

    def set_init(self, width, height, background_color, word_color, is_font_size_norm):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.word_color = word_color
        self.is_font_size_norm = is_font_size_norm

    def _draw_word_cloud(self, word2cnt):
        word_cloud = WordCloud(font_path=self.FONT_NAME,
                               width=self.width, height=self.height,
                               background_color=self.background_color)
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
        if type(data[0]) == list:
            temp = []
            for words in data:
                temp += words
            word2cnt = self.count_word(temp)
        elif type(data) == list:
            word2cnt = self.count_word(data)
        elif type(data) == dict:
            word2cnt = data
        else:
            print('Input type error (Input type : list[[str]] or list[] or str')
            raise ValueError

        return word2cnt

    def draw_word_cloud(self, data, width=1200, height=800, background_color='white',
                        ,word_color="standard", is_font_size_norm=False):

        # 기본값 세팅
        self.set_init(width=width, height=height, background_color=background_color,
                      word_color=word_color, is_font_size_norm=is_font_size_norm)

        # 입력 데이터 정규화 (list or list[list] or dict -> dict)
        word2cnt = self.normalize_input_data(data)

        # 워드클라우드 출력
        self._draw_word_cloud(word2cnt)


if __name__ == '__main__':
    corpus = [['dog', 'dog', 'cat', 'dog', 'cow', 'cat', 'phone'], ['dog', 'dog', 'cat'], ['coffee', 'dog', 'cat'], ['cow']]
    mwc = MyWordCloud()
    mwc.draw_word_cloud(corpus)
