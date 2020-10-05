import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


class MyWordCloud:
    def __init__(self):
        self.FILE_PATH = ''
        self.FILE_NAME = ''
        self.FONT_NAME = "./NanumSquareB.ttf"


    def draw_word_cloud(self, text, width=1600, height=800, background_color='white'):
        word_cloud = WordCloud(font_path=self.FONT_NAME,
                               max_font_size=100, min_font_size=10,
                               width=width, height=height,
                               background_color=background_color)
        word_cloud = word_cloud.generate_from_text(text)
        plt.imshow(word_cloud)
        plt.axis('off')
        plt.show()


data = "dog dog cat cat dog cat dog cat phone play move play"
mwc = MyWordCloud()
mwc.draw_word_cloud(data)

