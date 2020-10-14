import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud


class MyWordCloud:
    def __init__(self):
        self.FILE_PATH = ''
        self.FILE_NAME = ''
        self.FONT_NAME = "./NanumSquareB.ttf"

    def _draw_word_cloud(self, text, width=1600, height=800, background_color='white'):
        word_cloud = WordCloud(font_path=self.FONT_NAME,
                               max_font_size=100, min_font_size=10,
                               width=width, height=height,
                               background_color=background_color)
        word_cloud = word_cloud.generate_from_text(text)
        plt.imshow(word_cloud)
        plt.axis('off')
        plt.show()

    def draw_word_cloud(self, data, width=1600, height=800, background_color='white'):
        if type(data[0]) == list:
            data = [b for a in data for b in a]
            data = ' '.join(data)
        elif type(data) == list:
            data = ' '.join(data)
        elif type(data) == str:
            data = data
        else:
            print('Input type error (Input type : list[[str]] or list[] or str')

        self._draw_word_cloud(data, width=width, height=height, background_color=background_color)


if __name__ == '__main__':
    corpus = [['dog', 'dog', 'cat', 'dog', 'cow', 'cat', 'phone'], ['dog', 'dog', 'cat'], ['coffee', 'dog', 'cat'], ['cow']]
    mwc = MyWordCloud()
    mwc.draw_word_cloud(corpus)
