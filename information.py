import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import font_manager


# 기본 정보 출력 클래스
class Information:
    def __init__(self):
        self.SMALL_SIZE = 7

    def _set_kor_font(self):
        # 한글 폰트 설정
        self.FONT_PATH = "./NanumSquareB.ttf"
        self.FONT_NAME = font_manager.FontProperties(fname=self.FONT_PATH).get_name()
        plt.rc('font', family=self.FONT_NAME)

    # 데이터의 기본정보를 출력하는 함수
    @staticmethod
    def print_basic_info(data):
        """
        :param data: (DataFrame) data
        :return: None
        """
        print("Data shape : ", data.shape, end='\n\n')
        print(data.info(), end='\n\n')
        print("Data Null Sum Percent \n", round(data.isnull().sum()/data.shape[0] * 100, 2), end='\n\n')

    # 수치형 데이터의 평균, 중위값 등 기본적 통계 지표를 출력하는 함수
    @staticmethod
    def print_statistics_ind(data, col_name, qlt=False):
        """
        :param data: (DataFrame) data
        :param col_name: (str) Column name for which you want to see indicators
        :param qlt: (bool) If column is qualitative variable, this parameter is true
        :return: None
        """

        # 질적변수인 경우
        if qlt:
            print("Data category: ", data[col_name].unique())
            print("Data category: ", data[col_name].value_counts(sort=False).values)

            x_feature_ratio = data[col_name].value_counts(sort=False)
            x_feature_index = x_feature_ratio.index

            # x값 시각화
            plt.plot(aspect='auto')
            plt.pie(x_feature_ratio, labels=x_feature_index, autopct='%1.1f%%')
            plt.title(str(col_name) + '\'s ratio in total')

            plt.show()

        # 양적 변수인 경우
        else:
            print("Data Max : ", data[col_name].max())
            print("Data Min : ", data[col_name].min())
            print("Data Mean : ", data[col_name].mean())
            print("Data Median : ", data[col_name].median())
            print("Data Top 05% : ", np.percentile(data[col_name].values, 95))
            print("Data Top 25% : ", np.percentile(data[col_name].values, 75))
            print("Data Top 75% : ", np.percentile(data[col_name].values, 25))
            print("Data Top 95% : ", np.percentile(data[col_name].values, 5))
            print("Data Variance : {0: .3f}".format(data[col_name].var()))
            print("Data Standard deviation: {0: .3f}".format(data[col_name].std()))
            print()

            plt.subplot(1, 2, 1)
            plt.boxplot(data[col_name])

            plt.subplot(1, 2, 2)
            plt.hist(data[col_name])

            plt.show()


class Visualization:
    @staticmethod
    # 파이차트 시각화 함수
    def pie_chart(data, x_name, y_name=None):
        """
        :param data: (dataFrame) data
        :param x_name: (str) independent variable column name
        :param y_name: (str) dependent variable column name, default=None
        :return: None
        """
        x_feature_ratio = data[x_name].value_counts(sort=False)
        x_feature_size = x_feature_ratio.size
        x_feature_index = x_feature_ratio.index

        # x값 시각화
        plt.plot(aspect='auto')
        plt.pie(x_feature_ratio, labels=x_feature_index, autopct='%1.1f%%')
        plt.title(str(x_name) + '\'s ratio in total')

        plt.show()

        # 입력된 y값이 있을 경우
        if y_name is not None:
            y_feature_ratio = data[y_name].value_counts(sort=False)
            y_feature_index = y_feature_ratio.index

            # x, y값 DataFrame 정리
            xy_correlation_df = pd.DataFrame(columns=y_feature_index)
            for index in x_feature_index:
                xy_correlation_df.loc[index] = data[y_name][data[x_name] == index].value_counts()

            # 입력 x값 별 y값 시각화
            for i, index in enumerate(x_feature_index):
                plt.subplot(1, x_feature_size + 1, i + 1, aspect='equal')
                plt.pie(xy_correlation_df.loc[index], labels=y_feature_index, autopct='%1.1f%%')
                plt.title(str(index) + '\'s ratio')

            plt.show()

    # 바차트 시각화 함수
    def bar_chart(self, data, x_name, y_name=None, reversal=False):
        """
        :param data: (dataFrame) data
        :param x_name: (str) independent variable column name
        :param y_name: (str) dependent variable column name, default=None
        :param reversal: (bool) reverse x-axis, y-axis, default=False
        :return: None
        """
        x_feature_ratio = data[x_name].value_counts(sort=False)
        x_feature_size = x_feature_ratio.size
        x_feature_index = x_feature_ratio.index

        # x값 시각화
        plt.plot(aspect='auto')
        if reversal is True:
            plt.barh(x_feature_index, x_feature_ratio)
        else:
            plt.bar(x_feature_index, x_feature_ratio)
        plt.title(str(x_name))

        plt.show()

        # 입력된 y값이 있을 경우
        if y_name is not None:
            y_feature_ratio = data[y_name].value_counts(sort=False)
            y_feature_index = y_feature_ratio.index

            # x, y값 DataFrame 정리
            xy_correlation_df = pd.DataFrame(columns=y_feature_index)
            for index in x_feature_index:
                xy_correlation_df.loc[index] = data[y_name][data[x_name] == index].value_counts()

            # 입력 x값 별 y값 시각화
            for i, index in enumerate(x_feature_index):
                plt.subplot(1, x_feature_size + 1, i + 1, aspect='auto')
                if reversal is True:
                    plt.barh(y_feature_index, xy_correlation_df.loc[index])
                else:
                    plt.bar(y_feature_index, xy_correlation_df.loc[index])
                plt.title(str(index) + '\'s ratio')

            plt.show()
