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
        word2rep = self.load_util_json(name)

        # 요소 추가
        for k, v in elem:
            word2rep[k] = v

        # json 데이터 쓰기
        with open(self.UTIL_PATH + name, 'w') as f:
            json.dump(word2rep, f)


class TextProcessing(Utility):
    def __init__(self):
        super().__init__()

        # 기호별 유니코드
        self.comma = re.compile(r'[,᠂、︐︑﹐﹑፣꓾᠈߸꘍\u0326\uFF0C\uFF64]')
        self.colon = re.compile(r'[:˸܃܄፥᠄⁝∶꛴꞉﹕\uFF1A]')
        self.dash = re.compile(r'[\-\u2012-\u2015\u2053\u301C\u3030\uFF0D\uFF70]')
        self.elipse = re.compile(r'[…ຯ᠁ฯ⋮⋯⋰⋱︙]')
        self.exclamation = re.compile(
            r'[!\uFF01\u01C3\u203C\u2048\u2049\u26A0\u2755\u2757\u2762\u2763'
            r'\uA71D-\uA71F\uFE57\u055C\u07F9\u109F\u1944]')
        self.bullet = re.compile(
            r'[\u318D\u00B7\u0387\u05BC\u16EB\u2022\u2023\u2027\u2043\u204C\u204D'
            r'\u2218\u2219\u22C5\u23FA\u25CF\u25E6\u26AB\u2981\u2E30\u2E31\u2E33\u30FB\uA78F\uFF65]')
        self.hyphen = re.compile(
            r'[\u00AF\u2013\u2015\u2212\u00AD\u2010\u2011\u058A\u1806\u2E17\u30FB\uFE63\uFF0D\uFF65]')
        self.double_hyphen = re.compile(r'[=\u207C\u208C\u2A74\u1400\u2E17\u2E40\u30A0\uA78A\u3013\uFF1D]')
        self.question_mark = re.compile(
            r'[\u003F\u00BF\u055E\u061F\u2E2E\uFF1F\u1367\uA60F\u2047\uFE56\u2048\u2049'
            r'\u203D\u0294\uFFFD\u225F\u2A7B\u2A7C]')
        self.single_quotation_mark = re.compile(
            r'[\'ʻʽ،՝ʼ`\u00B4\u0312-\u0315\uA6F5\u2018\u2019\uFF07\uFF40]')
        self.double_quotation_mark = re.compile(r'[\u0022\u201E\u201C\u201D\uFF02\u3003\uE057]')
        self.corner_bracket_left = re.compile(r'[\u300C\uFE41\u300E\uFE43\uFF62]')
        self.corner_bracket_right = re.compile(r'[\u300D\uFE42\u300F\uFE44\uFF63]')
        self.round_bracket_left = re.compile(r'[(\uFE35]')
        self.round_bracket_right = re.compile(r'[)\uFE36]')
        self.angle_bracket_left = re.compile(r'[<\u3008\u2329\uFE3F\u300A\uFE3D\u3014\uFE5D]')
        self.angle_bracket_right = re.compile(r'[>\u3009\u232A\uFE40\u300B\uFE3E\u3015\uFE5E]')
        self.box_bracket_left = re.compile(r'[\[\u3010\uFE3B\uFF3B]')
        self.box_bracket_right = re.compile(r'[]\u3011\uFE3C\uFF3D]')
        self.fullstop = re.compile(r'[.\u00B0\u3002\uFE12\uFE52\uFF61\uFF0E]')
        self.white_space = re.compile(r'[\u0020\u00A0\u1680\u2000-\u200A\u202F\u205F\u3000\u3164\uFFA0]')
        self.ascii_symbol = re.compile(r'[\u0021-\u002F\u003A-\u0040\u005B-\u0060\u007B-\u007E]')

        # 언어별 유니코드 범위
        self.latin = re.compile(r'[\u00C0-\u02AF]')
        self.greek = re.compile(r'[\u0370-\u03FF\u1F00-\u1FFF]')
        self.russian = re.compile(
            r'[\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69F\u1C80-\u1C8F\u1D2B\u1D78\uFE2E-\uFE2F]')
        self.korean_whole = re.compile(r'[ㄱ-ㅎㅏ-ㅣ가-힣]')
        self.korean = re.compile(r'[가-힣]')
        self.chinese = re.compile(
            r'[\u4E00-\u9FFF\u3400-\u4DBF\u2000-\u2A6D\u2A70-\u2B73\u2B74-\u2B81'
            r'\u2B82-\u2CEA\uF900-\uFAFF\u2F80-\u2FA1]')
        self.japanese = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')
        self.arabic = re.compile(
            r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\u10E60-'
            r'\u10E7\u1EC7-\u1ECB\u1EE0-\u1EEF]')

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
        self.html_tags = ['<em>', '</em>', '<e m>', '<br>', '</br>']

        # 자주 쓰이는 밈 표현
        self.meme = [r'ㅋ+', r'ㅎ+', r'ㅜ+', r'\^\^', r':\)', r'~+', r'!+']

        self.unicode_full2half = self.load_util_json('unicode_full2half.json')
        self.grammar_typo2cor = self.load_util_json('grammar_typo2cor.json')
        self.grammar_en2kr = self.load_util_json('grammar_en2kr.json')
        self.kiwi_tag2pos = self.load_util_json('kiwi_tag2pos.json')    # 긍정지시사: ~이다 / 부정지시가: ~아니다

    # 영어로된 kiwi 태그를 한국어 형태소로 변환하는 함수
    def convert_tag2pos(self, s):
        return self.kiwi_tag2pos[s]

    # FullWidth(전자) 문자를 HalfWidth(반자) 문자로 변환해주는 메서드
    def convert_full_to_half(self, df, col):
        """
        :param df: (DataFrame) data
        :param col: (str or list) column name or columns name
        :return: converted data to half width from full width
        """
        return df.replace({col: self.unicode_full2half})

    # HTML Tag 제거 메서드
    def remove_html_tags(self, df, col):
        """
        :param df: (DataFrame) data
        :param col: (str or list) column name or columns name
        :return: converted data to half width from full width
        """
        for tag in self.html_tags:
            df[col] = df[col].str.replace(tag, " ")

        return df

    # 특수문자 제거 메서드
    def remove_special_char(self, df, col):
        """
        :param df: (DataFrame) data
        :param col: (str or list) column name or columns name
        :return: converted data to half width from full width
        """
        for tag in self.html_tags:
            df[col] = df[col].str.replace(tag, " ")

        return df

    # 맞춤법 교정 메서드
    def correct_grammar(self, df, col):
        """
        :param df: (DataFrame) data
        :param col: (str or list) column name or columns name
        :return: converted data to half width from full width
        """
        for k, v in self.grammar_typo2cor.items():
            df[col] = df[col].str.replace(k, v)

        return df

    # 자주 쓰는 영어 표현을 한국어로 변환하는 메서드
    def convert_en_to_kr(self, df, col):
        """
        :param df: (DataFrame) data
        :param col: (str or list) column name or columns name
        :return: converted data to half width from full width
        """
        for en, kr in self.grammar_en2kr.items():
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
        for v in self.meme:
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
