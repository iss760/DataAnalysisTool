import json
import re


class Utility:
    def __init__(self):
        self.UTIL_PATH = './utility/'

    # json 불러오는 메서드
    def load_util_json(self, name) -> json:
        """
        :param name: (str) load file name
        :return: (json) loaded json
        """
        with open(self.UTIL_PATH + name, 'r') as f:
            return json.load(f)

    # json 사전에 요소(element) 추가해주는 메서드
    def add_util_json(self, name, elem):
        """
        :param name: (str) the json name to which the element to add belongs
        :param elem: (dict) elements to be added
        :return: None
        """
        # json 데이터 읽기
        try:
            word2rep = self.load_util_json(name)
        except FileNotFoundError:
            word2rep = {}

        # 요소 추가
        for k, v in elem.items():
            word2rep[k] = v

        # json 데이터 쓰기
        with open(self.UTIL_PATH + name, 'w') as f:
            json.dump(word2rep, f)


class TextProcessing(Utility):
    def __init__(self):
        super().__init__()

        # 언어별 실 사용 유니코드 범위
        self.not_en = re.compile(r'[^A-Za-z0-9.,\'!?#\u0020\n]')
        self.not_ko = re.compile(r'[^.,!?#\u0020\n가-힣]')
        self.not_ko_en = re.compile(r'[^A-Za-z0-9.,!?#\u0020\n가-힣]')
        self.not_latin_en = re.compile(r'[^A-Za-z0-9.,\'!?#\u0020\n\u00C0-\u02AF]')
        self.not_cn_en = re.compile(
            r'[^A-Za-z0-9.,\'!?#\u0020\n\u4E00-\u9FFF\u3400-\u4DBF\u2000-\u2A6D\u2A70-\u2B73'
            r'\u2B740-\u2B81\u2B820-\u2CEA\uF900-\uFAFF\u2F80-\u2FA1]')
        self.not_cn_jp_en = re.compile(
            r'[^A-Za-z0-9.,\'!?#\u0020\n\u4E00-\u9FFF\u3400-\u4DBF\u2000-\u2A6D\u2A70-\u2B73'
            r'\u2B74-\u2B81\u2B82-\u2CEA\uF900-\uFAFF\u2F80-\u2FA1\u3040-\u309F\u30A0-\u30FF]')
        self.not_ru_en = re.compile(
            r'[^A-Za-z0-9.,\'!?#\u0020\n\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69F\u1C80-'
            r'\u1C8F\u1D2B\u1D78\uFE2E-\uFE2F]')
        self.not_gr_en = re.compile(r'[^A-Za-z0-9.,\'!?#\u0020\n\u0370-\u03FF\u1F00-\u1FFF]')
        self.not_arabic_en = re.compile(
            r'[^A-Za-z0-9.,\'!?#\u0020\n\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF'
            r'\uFE70-\uFEFF\u10E6-\u10E7\u1EC7-\u1ECB\u1EE0-\u1EEF]')

        # HTML 모음
        self.HTML_TAGS = ['<em>', '</em>', '<br>', '</br>']

        # 자주 쓰이는 밈 표현
        self.MEME = [r'ㅋ+', r'ㅎ+', r'ㅜ+', r'\^\^', r':\)', r'~+', r'!+']

        # 언어별 유니코드 범위 (언어: re.compile(유니코드 범위))
        # keys: latin, greek, russian, korean_whole, korean, chinese, japanese, arabic
        self.REX_LANGUAGE2UNICODE = self.load_util_json('rex_language2unicode.json')
        self.REX_LANGUAGE2UNICODE = dict(map(lambda x: (x[0], re.compile(x[1])), self.REX_LANGUAGE2UNICODE.items()))

        # 기호별 유니코드 (특수기호: re.compile(유니코드들))
        # keys : comma, colon, dash, exclamation, bullet, hyphen, double_hyphen, question_mark, single_quotation_mark,
        #        corner_bracket_left, corner_bracket_right, round_bracket_left, angle_bracket_left, angle_bracket_right,
        #        box_bracket_left, box_bracket_right, full_stop, white_space, ascii_symbol
        self.REX_SYMBOL2UNICODE = self.load_util_json('rex_symbol2unicode.json')
        self.REX_SYMBOL2UNICODE = dict(map(lambda x: (x[0], re.compile(x[1])), self.REX_SYMBOL2UNICODE.items()))

        # 전각 반자 유니코드 (전각: 반자)
        self.UNICODE_FULL2HALF = self.load_util_json('unicode_full2half.json')

        # 자주 쓰이는 오타와 정답 (오타: 정답)
        self.GRAMMAR_TYPO2COR = self.load_util_json('grammar_typo2cor.json')

        # 자주 쓰이는 축약어(한자 포함)의 오리지날 표현 (축약어: 오리지날)
        self.GRAMMAR_ABBR2COR = self.load_util_json('grammar_abbr2cor.json')

        # 자주 쓰이는 영어표현의 한국어 표현 (영어: 한국어)
        self.GRAMMAR_EN2KR = self.load_util_json('grammar_en2kr.json')

        # 키위 형태소 분석기의 형태소 영어명과 한국명 (형태소 영어명: 형태소 한국명)
        self.KIWI_TAG2POS = self.load_util_json('kiwi_tag2pos.json')    # 긍정지시사: ~이다 / 부정지시가: ~아니다

    # 특수기호 유니코드 정규화 메서드
    def normalize_special_symbol(self, doc):
        pass

    # 영어로된 kiwi 태그를 한국어 형태소로 변환하는 함수
    def convert_tag2pos(self, s):
        return self.KIWI_TAG2POS[s]

    # FullWidth(전자) 문자를 HalfWidth(반자) 문자로 변환해주는 메서드
    def convert_full_to_half(self, df, col):
        """
        :param df: (DataFrame) data
        :param col: (str or list) column name or columns name
        :return: converted data to half width from full width
        """
        return df.replace({col: self.UNICODE_FULL2HALF})

    # HTML Tag 제거 메서드
    def remove_html_tags(self, df, col):
        """
        :param df: (DataFrame) data
        :param col: (str or list) column name or columns name
        :return: converted data to half width from full width
        """
        for tag in self.HTML_TAGS:
            df[col] = df[col].str.replace(tag, " ")

        return df

    # 특수문자 제거 메서드
    def remove_special_char(self, df, col):
        """
        :param df: (DataFrame) data
        :param col: (str or list) column name or columns name
        :return: converted data to half width from full width
        """
        for tag in self.HTML_TAGS:
            df[col] = df[col].str.replace(tag, " ")

        return df

    # 맞춤법 교정 메서드
    def correct_grammar(self, df, col):
        """
        :param df: (DataFrame) data
        :param col: (str or list) column name or columns name
        :return: converted data to half width from full width
        """
        for k, v in self.GRAMMAR_TYPO2COR.items():
            df[col] = df[col].str.replace(k, v)

        return df

    # 자주 쓰는 영어 표현을 한국어로 변환하는 메서드
    def convert_en_to_kr(self, df, col):
        """
        :param df: (DataFrame) data
        :param col: (str or list) column name or columns name
        :return: converted data to half width from full width
        """
        for en, kr in self.GRAMMAR_EN2KR.items():
            df[col].replace(to_replace=en, value=kr, regex=True, inplace=True)

        return df

    # 자주 쓰는 밈을 형태소 분석이 가능하도록 변환하는 메서드
    # 밈은 ㅋㅋㅋ, ㅎ, ^^ 등을 모두 포함함
    def remove_meme(self, df, col):
        """
        :param df: (DataFrame) data
        :param col: (str or list) column name or columns name
        :return: converted data to half width from full width
        """
        for v in self.MEME:
            df[col].replace(to_replace='', value=v, regex=True, inplace=True)

        return df

    # 영어로만 이루어진 데이터(행) 제거 메서드
    def remove_only_en(self, df, col):
        temp = df[col].str.contains(r'[A-Za-z]')
        temp = df[temp]
        print(temp[col].values)

    def unicode_norm(self):
        pass


class Filtering:
    def __init__(self):
        self.FILE_PATH = ""
        self.FILE_NAME = ""
        self.FILTERING_FILE_PATH = ""
        self.FILTERING_FILE_NAME = ""
        self.FILTERING_KEYWORD = []

    def make_filtering_keyword(self, path, name):
        self.FILE_PATH = path
        self.FILE_NAME = name

    def filtering(self, data, col_name):
        data = data[~data[col_name].str.contains('|'.join(self.FILTERING_KEYWORD), na=False)]


if __name__ == '__main__':
    tp = TextProcessing()
    print(tp.GRAMMAR_ABBR2COR)

    # tp.add_util_json('grammar_abbr2cor.json', tp.GRAMMAR_ABBR2COR)
    # print(tp.GRAMMAR_ABBR2COR.keys())
    # for k, v in tp.GRAMMAR_ABBR2COR.items():
    #     print(k, v)
