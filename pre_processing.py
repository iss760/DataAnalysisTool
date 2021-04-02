import numpy as np
import pandas as pd


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
