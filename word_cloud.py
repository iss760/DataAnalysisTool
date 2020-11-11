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

        self.word_pool = []
        self.n_top = 100

    def set_init(self, width, height, background_color, is_font_size_norm, word_pool, n_top):
        self.width = width
        self.height = height
        self.background_color = background_color

        self.color_func = None
        self.is_font_size_norm = is_font_size_norm

        self.word_pool = word_pool
        self.n_top = n_top

    def set_color_func(self, word_color):
        if word_color == 'similar':
            self.color_func = self._similar_color_func
        elif word_color == 'multi':
            self.color_func = self._multi_color_func
        else:
            self.color_func = None

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

    def _count_word(self, data):
        # 딕셔너리 만들기
        word2cnt = {}
        for word in data:
            if word not in word2cnt.keys():
                word2cnt[word] = 1
            else:
                word2cnt[word] += 1

        # 딕셔너리 정렬
        sorted(word2cnt.items(), key=lambda x: x[1], reverse=True)

        return word2cnt

    def conversion_to_dict(self, data):
        if type(data) not in (dict, list):
            print('Input type error (Input type: dict or list[[str]] or list[str]')
            raise ValueError
        else:
            if type(data) == dict:
                word2cnt = data
            elif type(data[0]) == list:
                # 하나의 리스트로 결합
                temp = []
                for words in data:
                    temp += words
                word2cnt = self._count_word(temp)    # 딕셔너리로 변환
            elif type(data) == list:
                word2cnt = self._count_word(data)    # 딕셔너리로 변환
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

    def extract_from_word_pool(self, data):
        for k, v in data.items():
            if v not in self.word_pool:
                del data[k]
        return data

    def extract_n_top_word(self, data):
        res = {}
        size = min(self.n_top, len(data.keys()))
        for i, (k, v) in enumerate(data.items()):
            res[k] = v
            if i >= size - 1:
                break
        return res

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

    def draw_word_cloud(self, data, width=1200, height=800, background_color='white',
                        word_color="standard", is_font_size_norm=False, word_pool=None, n_top=100):
        # 기본값 세팅
        self.set_init(width=width, height=height, background_color=background_color,
                      is_font_size_norm=is_font_size_norm, word_pool=word_pool, n_top=n_top)

        # 워드클라우드 글자색 선택 (standard or similar or multi)
        self.set_color_func(word_color)

        # 입력 데이터 형변환 (list or list[list] or dict -> dict)
        word2cnt = self.conversion_to_dict(data)

        # 입력 데이터 정규화 (워드간 수치의 분산이 클 경우)
        if is_font_size_norm:
            word2cnt = self.normalize_data(word2cnt)

        # 주어진 word pool(워드클라우드에 담길 워드들)이 있을 때, 주어진 word pool로 word cloud 구성
        if word_pool is not None:
            word2cnt = self.extract_from_word_pool(word_pool)

        word2cnt = self.extract_n_top_word(word2cnt)

        # 워드클라우드 출력
        self._draw_word_cloud(word2cnt)


if __name__ == '__main__':
    corpus = [['dog', 'dog', 'cat', 'dog', 'cow', 'cat', 'tiger'], ['dog', 'dog', 'cat'], ['cow']]
    #dic = {'dog': 10, 'cat': 6, 'horse': 5, 'cow': 4, 'rabbit': 7, 'tiger': 2}
    mwc = MyWordCloud()
    mwc.draw_word_cloud(corpus, word_color='multi', is_font_size_norm=True)
