from konlpy.tag import Okt
from time import sleep


class Tokenizer:
    def __init__(self):
        self.okt = Okt()
        self.STOP_WORD = []
        self.SLEEP_INTERVAL = 0
        self.MIN_LEN = 0

    # 불용어 생성 함수
    def make_stop_word(self, stop_word):
        self.STOP_WORD = stop_word

    # 최소 형태소 길이 생성 함수
    def make_min_len(self, min_len):
        self.MIN_LEN = min_len

    # 형태소 분석 중 쉬는 간격 생성 함수
    def make_sleep_interval(self, sleep_interval):
        self.SLEEP_INTERVAL = sleep_interval

    def _tokenizer(self, sentence, tkn_method, stem=False, norm=False):
        sentence = str(sentence)
        if tkn_method == 'pos':
            temp = self.okt.pos(sentence, stem=stem, norm=norm)
            return [[word, pos] for word, pos in temp if word not in self.STOP_WORD and len(word) > self.MIN_LEN]

        if tkn_method == 'morphs':
            temp = self.okt.morphs(sentence, stem=stem, norm=norm)
        elif tkn_method == 'none':
            temp = self.okt.nouns(sentence)
        else:
            temp = None

        return [word for word in temp if word not in self.STOP_WORD and len(word) > self.MIN_LEN]

    # 하나의 문장 또는 복수개의 문장 형태소 분석 함수
    def tokenizer(self, data, tkn_method='morphs', stem=False, norm=False):
        """
        :param data: 형태소 분석할 데이터, str or list[str]
        :param tkn_method: 형태소 분석 방법, str
        :param stem: stemming 유무, bool
        :param norm: normalization 유무, bool
        :return: 토크나이징 된 문장 or 문장들, list[str] or list[[str]] or list[[(str, str)]]
        """
        # 형태소 분석 방식 검사
        if tkn_method not in ('pos', 'morphs', 'nouns'):
            print('tokenizer value error')
            raise ValueError

        # 입력값이 하나의 문장일 경우
        if type(data) is str:
            tokenized_sentence = self._tokenizer(data, tkn_method=tkn_method, stem=stem, norm=norm)
            return tokenized_sentence

        # 입력값이 복수개의 문장일 경우
        elif type(data) is list:
            tokenized_sentences = []
            for i, sentence in enumerate(data):
                sentence = str(sentence)

                # 메모리 에러 방지를 위한 sleep
                if self.SLEEP_INTERVAL > 0 and i % self.SLEEP_INTERVAL:
                    sleep(3)

                tokenized_sentence = self._tokenizer(sentence, tkn_method=tkn_method, stem=stem, norm=norm)
                tokenized_sentences.append(tokenized_sentence)

            return tokenized_sentences

        else:
            print("data type error")
            raise ValueError


tkn = Tokenizer()
print(tkn.tokenizer(['나는 무엇으로 사는가?', '이거 맛있네'], tkn_method='morphs'))
