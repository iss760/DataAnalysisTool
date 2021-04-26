import numpy as np
import pandas as pd

import re


class NumericalTypeProcessing:
    def get_outlier(self, data, col_name, weight=1.5):
        q1 = np.percentile(data[col_name].values, 25)
        q3 = np.percentile(data[col_name].values, 75)
        iqr = q3 - q1

        iqr_weight = iqr * weight
        lowest = q1 - iqr_weight
        highest = q3 + iqr_weight

        outlier_idx = data[col_name][(data[col_name] < lowest) | (data[col_name] > highest)].index
        return outlier_idx

    def remove_outlier_use_iqr(self, data, col_name, weight=1.5):
        outlier_idx = self.get_outlier(data, col_name=col_name, weight=weight)    # 이상치 탐색
        data.drop(outlier_idx, axis=0, inplace=True)    # 이상치 제거
        return data


class TextTypeProcessing:
    def __init__(self):
        # 기호별 유니코드
        self.comma = re.compile(r'[᠂、︐︑﹐﹑፣꓾᠈߸꘍\u0326\uFF0C\uFF64]')
        self.colon = re.compile(r'[:˸܃܄፥᠄⁝∶꛴꞉﹕\uFF1A]')
        self.dash = re.compile(r'[\-\u2012-\u2015\u2053\u301C\u3030\uFF0D\uFF70]')
        self.elipse = re.compile(r'[…ຯ᠁ฯ⋮⋯⋰⋱︙]')
        self.exclamation = re.compile(
            r'[!\uFF01\u01C3\u203C\u2048\u2049\u26A0\u2755\u2757\u2762\u2763\uA71D-\uA71F\uFE57\u055C\u07F9\u109F\u1944]')
        self.bullet = re.compile(
            r'[\u318D\u00B7\u0387\u05BC\u16EB\u2022\u2023\u2027\u2043\u204C\u204D\u2218\u2219\u22C5\u23FA\u25CF\u25E6\u26AB\u2981\u2E30\u2E31\u2E33\u30FB\uA78F\uFF65]')
        self.hypen = re.compile(
            r'[\u00AF\u2013\u2015\u2212\u00AD\u2010\u2011\u058A\u1806\u2E17\u30FB\uFE63\uFF0D\uFF65]')
        self.double_hypen = re.compile(r'[=\u207C\u208C\u2A74\u1400\u2E17\u2E40\u30A0\uA78A\u3013\uFF1D]')
        self.question_mark = re.compile(
            r'[\u003F\u00BF\u055E\u061F\u2E2E\uFF1F\u1367\uA60F\u2047\uFE56\u2048\u2049\u203D\u0294\uFFFD\u225F\u2A7B\u2A7C]')
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
            r'[\u4E00-\u9FFF\u3400-\u4DBF\u20000-\u2A6DF\u2A700-\u2B73F\u2B740-\u2B81F\u2B820-\u2CEAF\uF900-\uFAFF\u2F800-\u2FA1F]')
        self.japanese = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')
        self.arabic = re.compile(
            r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\u10E60-\u10E7F\u1EC70-\u1ECBF\u1EE00-\u1EEFF]')

        # 언어별 실 사용 유니코드 범위
        self.not_en = re.compile(r'[^A-Za-z0-9.,\'!?#\u0020\n]')
        self.not_ko = re.compile(r'[^.,!?#\u0020\n가-힣]')
        self.not_ko_en = re.compile(r'[^A-Za-z0-9.,!?#\u0020\n가-힣]')
        self.not_latin_en = re.compile(r'[^A-Za-z0-9.,\'!?#\u0020\n\u00C0-\u02AF]')
        self.not_cn_en = re.compile(
            r'[^A-Za-z0-9.,\'!?#\u0020\n\u4E00-\u9FFF\u3400-\u4DBF\u20000-\u2A6DF\u2A700-\u2B73F\u2B740-\u2B81F\u2B820-\u2CEAF\uF900-\uFAFF\u2F800-\u2FA1F]')
        self.not_cn_jp_en = re.compile(
            r'[^A-Za-z0-9.,\'!?#\u0020\n\u4E00-\u9FFF\u3400-\u4DBF\u20000-\u2A6DF\u2A700-\u2B73F\u2B740-\u2B81F\u2B820-\u2CEAF\uF900-\uFAFF\u2F800-\u2FA1F\u3040-\u309F\u30A0-\u30FF]')
        self.not_ru_en = re.compile(
            r'[^A-Za-z0-9.,\'!?#\u0020\n\u0400-\u04FF\u0500-\u052F\u2DE0-\u2DFF\uA640-\uA69F\u1C80-\u1C8F\u1D2B\u1D78\uFE2E-\uFE2F]')
        self.not_gr_en = re.compile(r'[^A-Za-z0-9.,\'!?#\u0020\n\u0370-\u03FF\u1F00-\u1FFF]')
        self.not_arabic_en = re.compile(
            r'[^A-Za-z0-9.,\'!?#\u0020\n\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\u10E60-\u10E7F\u1EC70-\u1ECBF\u1EE00-\u1EEFF]')

        # 의외로 자주 사용되는 HalfWidth(반자), FullWidth(전자) unicode 변환을 위한 딕셔너리
        self.unicode_full2half = {
            '\uFE01': '!',
            '\uFF02': '"',
            '\uFF03': '/',
            '\uFF04': '$',
            '\uFF05': '%',
            '\uFF06': '&',
            '\uFF07': "'",
            '\uFF08': '(',
            '\uFF09': ')',
            '\uFF0A': '*',
            '\uFF0B': '+',
            '\uFF0C': ',',
            '\uFF0D': '-',
            '\uFF0E': '.',
            '\uFF0F': '/',
            '\uFF10': '0',
            '\uFF11': '1',
            '\uFF12': '2',
            '\uFF13': '3',
            '\uFF14': '4',
            '\uFF15': '5',
            '\uFF16': '6',
            '\uFF17': '7',
            '\uFF18': '8',
            '\uFF19': '9',
            '\uFF1A': ':',
            '\uFF1B': ';',
            '\uFF1C': '<',
            '\uFF1D': '=',
            '\uFF1E': '>',
            '\uFF1F': '?',
            '\uFF20': '@',
            '\uFF21': 'A',
            '\uFF22': 'B',
            '\uFF23': 'C',
            '\uFF24': 'D',
            '\uFF25': 'E',
            '\uFF26': 'F',
            '\uFF27': 'G',
            '\uFF28': 'H',
            '\uFF29': 'I',
            '\uFF2A': 'J',
            '\uFF2B': 'K',
            '\uFF2C': 'L',
            '\uFF2D': 'M',
            '\uFF2E': 'N',
            '\uFF2F': 'O',
            '\uFF30': 'P',
            '\uFF31': 'Q',
            '\uFF32': 'R',
            '\uFF33': 'S',
            '\uFF34': 'T',
            '\uFF35': 'U',
            '\uFF36': 'V',
            '\uFF37': 'W',
            '\uFF38': 'X',
            '\uFF39': 'Y',
            '\uFF3A': 'Z',
            '\uFF3B': '[',
            '\uFF3C': '\\',
            '\uFF3D': ']',
            '\uFF3E': '^',
            '\uFF3F': '_',
            '\uFF40': "'",
            '\uFF41': 'a',
            '\uFF42': 'b',
            '\uFF43': 'c',
            '\uFF44': 'd',
            '\uFF45': 'e',
            '\uFF46': 'f',
            '\uFF47': 'g',
            '\uFF48': 'h',
            '\uFF49': 'i',
            '\uFF4A': 'j',
            '\uFF4B': 'k',
            '\uFF4C': 'l',
            '\uFF4D': 'm',
            '\uFF4E': 'n',
            '\uFF4F': 'o',
            '\uFF50': "p",
            '\uFF51': 'q',
            '\uFF52': 'r',
            '\uFF53': 's',
            '\uFF54': 't',
            '\uFF55': 'u',
            '\uFF56': 'v',
            '\uFF57': 'w',
            '\uFF58': 'x',
            '\uFF59': 'y',
            '\uFF5A': 'z',
            '\uFF5B': '{',
            '\uFF5C': '|',
            '\uFF5D': '}',
            '\uFF5E': '~',
            '\uFF5F': '(',
            '\uFF60': ')',
            '\uFF61': '.',
            '\uFF62': '<',
            '\uFF63': '>',
            '\uFF64': ',',
            '\uFF65': ',',
            '\uFFE0': '\u00A2',
            '\uFFE1': '\u00A3',
            '\uFFE3': '-',
            '\uFFE4': '|',
            '\uFFE5': '\u00A5',
            '\uFFE6': '\u20A9',
            '\uffE8': '|'
        }

        # HTML 모음
        self.html_tags = ['<em>', '</em>', '<br>', '</br>']

    # FullWidth(전자) 문자를 HalfWidth(반자) 문자로 변환해주는 메서드
    def convert_full_to_half(self, df, col):
        """
        :param df: (DataFrame) data
        :param col: (str or list) column name or columns name
        :return: converted data to half width from full width
        """
        return df.replace({col: self.unicode_full2half})

    # HTML Tag 제거 메서드
    def remove_html_cd(self, df, col):
        """
        :param df: (DataFrame) data
        :param col: (str or list) column name or columns name
        :return: converted data to half width from full width
        """
        temp_dict = dict()
        for tag in self.html_tags:
            temp_dict[tag] = " "

        return df.replace({col: temp_dict})


    def unicode_norm(self):



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
