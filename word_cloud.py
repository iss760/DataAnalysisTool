import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud


class MyWordCloud:
    def __init__(self):
        self.FILE_PATH = ''
        self.FILE_NAME = ''
        self.FONT_NAME = "./NanumSquareB.ttf"

    def _draw_word_cloud(self, word2cnt, width=1200, height=800, background_color='white'):
        word_cloud = WordCloud(font_path=self.FONT_NAME,
                               width=width, height=height,
                               background_color=background_color)
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

    def draw_word_cloud(self, data, width=1200, height=800, background_color='white',
                        is_font_size_norm=False, word_color="standard"):
        if type(data[0]) == list:
            temp = []
            for words in data:
                temp += words
            word2cnt = self.count_word(data)
        elif type(data) == list:
            word2cnt = self.count_word(data)
        elif type(data) == dict:
            word2cnt = data
        else:
            print('Input type error (Input type : list[[str]] or list[] or str')

        self._draw_word_cloud(word2cnt, width=width, height=height, background_color=background_color)


if __name__ == '__main__':
    corpus = [['dog', 'dog', 'cat', 'dog', 'cow', 'cat', 'phone'], ['dog', 'dog', 'cat'], ['coffee', 'dog', 'cat'], ['cow']]
    mwc = MyWordCloud()
    mwc.draw_word_cloud(corpus)
