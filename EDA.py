import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import font_manager
import seaborn as sns


# 한글 폰트 설정 함수
def set_kor_font():
    # 한글 폰트 설정
    font_path = "font/NanumSquareB.ttf"
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    plt.rc('font', family=font_name)


# Null 값 정보를 얻는 함수
def print_null_info(df):
    """
    :param df: (DataFrame) Null 값 정보를 계산할 데이터
    :return: None
    """
    n_rows = df.shape[0]
    res_df = pd.DataFrame(df.isna().sum(), columns=['Null Cnt'])
    res_df['Non-Null Cnt'] = res_df['Null Cnt'].apply(lambda x: n_rows - x)
    res_df['Non-Null Ratio'] = res_df['Non-Null Cnt'].apply(lambda x: x / n_rows * 100)
    print(res_df)


# IQR 관련 값을 주는 함수
def _get_iqr(data):
    """
    :param data: (Series) IQR 계산할 데이터
    :return: (dict) Q1, Q3, IQR, Median, Min, Max 값
    """
    q1, q3 = np.percentile(data, [25, 75])
    iqr = q3 - q1
    res = {'q1': q1, 'q3': q3, 'iqr': iqr, 'median': data.median(),
           'min': q1 - (1.5 * iqr), 'max': q3 + (1.5 * iqr)}
    res = {k: round(v, 2) for k, v in res.items()}
    return res


# 박스플롯을 그려주는 함수
def show_box(df, cols, clf_col=None):
    """
    :param df: (DataFrame) 박스플롯을 그릴 데이터
    :param cols: (list[str]) 박스플롯을 그릴 데이터의 칼럼들 (수치형 데이터)
    :param clf_col (str) 클래스별 박스플롯을 그릴 경우, 클래스 칼럼
    :return: None
    """
    # 칼럼 입력 값 형 처리
    cols = [cols] if type(cols) is str else cols

    # 연속형 변수 박스플롯 그리기
    fig, axs = plt.subplots(1, len(cols), figsize=[3 * len(cols), 6])
    for i, col in enumerate(cols):
        # 복수 차트 or 단수 차트 처리
        _axs = axs[i] if type(axs) is np.ndarray else axs

        if clf_col is not None:
            # 박스플롯 그리기
            p = sns.boxplot(x=clf_col, y=col, data=df, orient='v', ax=axs[i])

            # 테이블 그리기
            iqr_df = pd.DataFrame(index=['q1', 'q3', 'iqr', 'median', 'min', 'max'])
            for j, c in enumerate(df[clf_col].unique()):
                iqr_df[c] = _get_iqr(df[df[clf_col] == c][col]).values()
            t = _axs.table(cellText=iqr_df.values,
                           colLabels=list(iqr_df.columns),
                           rowLabels=list(iqr_df.index),
                           bbox=[0.2, -0.6, 0.8, 0.4])
            # 테이블 폰트 사이즈 조정
            t.auto_set_font_size(False)
            t.set_fontsize(8)
        else:
            # 박스플롯 그리기
            p = sns.boxplot(y=col, data=df, orient='v', ax=_axs)

            # 테이블 그리기
            iqr_dict = _get_iqr(df[col])
            t = _axs.table(np.array(list(iqr_dict.values())).reshape(-1, 1),
                           rowLabels=list(iqr_dict.keys()),
                           bbox=[0.2, -0.6, 0.8, 0.4])
            # 테이블 폰트 사이즈 조정
            t.auto_set_font_size(False)
            t.set_fontsize(8)

        p.set(ylabel='')
        _axs.set_title(col)

    fig.tight_layout()
    plt.show()


# 파이차트를 그려주는 함수
def show_pie(df, cols, reverse_color=False):
    """
    :param df: (DataFrame) 파이차트를 그릴 데이터
    :param cols: (list[str] or str) 파이차트를 그릴 데이터의 칼럼들 (수치형 데이터)
    :param reverse_color: (bool) 제목, 라벨, 수치 컬러를 화이트로 할지 여부
    :return: None
    """
    # 칼럼 입력 값 형 처리
    cols = [cols] if type(cols) is str else cols

    # 범주형 변수 파이차트 그리기
    fig, axs = plt.subplots(1, len(cols), figsize=[3 * len(cols), 6])

    for i, col in enumerate(cols):
        # 카테고리별 개수 내림차순 정렬
        df_cnt = df[col].value_counts().sort_index(ascending=True)

        # 복수 차트 or 단수 차트 처리
        _axs = axs[i] if type(axs) is np.ndarray else axs

        # 파이차트 그리기
        _axs.pie(df_cnt,
                 autopct='%.1f%%',
                 labels=df_cnt.index,
                 textprops={'color': "w" if reverse_color is True else 'black'})
        _axs.set_title(col, color='w' if reverse_color is True else 'black')

        # 테이블 그리기
        t = _axs.table(np.array(df_cnt.values.tolist()).reshape(-1, 1),
                       rowLabels=df_cnt.index,
                       bbox=[0.2, -0.5, 0.8, 0.5],
                       cellLoc='center')
        # 테이블 폰트 사이즈 조정
        t.auto_set_font_size(False)
        t.set_fontsize(8)

    fig.tight_layout()
    plt.show()


def show_bar(df, cols):
    """
    :param df: (DataFrame) 바 차트를 그릴 데이터
    :param cols: (list[str] or str) 바 차트를 그릴 데이터의 칼럼명 들 (카디널리티가 작은 범주형 데이터)
    :return: None
    """
    # 칼럼 입력 값 형 처리
    cols = [cols] if type(cols) is str else cols

    cnt = 0
    for col in cols:
        cnt += len(df[col].unique())

    # 범주형 변수 바차트 그리기
    fig, axs = plt.subplots(1, len(cols), figsize=[cnt, 4])

    for i, col in enumerate(cols):
        # 카테고리별 개수 오름차순 정렬
        df_cnt = df[col].value_counts().sort_index(ascending=True)

        # 컬러 설정
        colors = sns.color_palette('dark')

        # 복수 차트 or 단수 차트 처리
        _axs = axs[i] if type(axs) is np.ndarray else axs

        # 바차트 그리기
        _axs.bar(x=df_cnt.index,
                 height=df_cnt.values,
                 color=colors)
        _axs.set_title(col, color='black')

        # 바차트에 숫자 추가
        for j, v in enumerate(df_cnt.index):
            _axs.text(v, df_cnt.values[j], df_cnt.values[j],
                      fontsize=8,
                      horizontalalignment='center',
                      verticalalignment='bottom')

    fig.tight_layout()
    plt.show()


def show_scatter(df, cols, hue=None, max_per_class=1000):
    if hue is None:
        pass

    if hue is not None:
        classes = df['hue'].unique()
        sample_df = pd.concat([df[df[c]] for c in classes])


# 변수의 분포를 보여주는 함수
def show_distribution(df, col):
    """
    :param df: (DataFrame) 데이터
    :param col: (str) 분포를 볼 칼럼
    :return: None
    """
    # 카디널리티 계산
    cardinality = len(df[col].unique())

    # 카디널리티가 작은 경우 (범주형에 가까운)
    if cardinality < 20:
        fig, axs = plt.subplots(1, 2, figsize=(4 + cardinality, 4))

        # 파이차트, 바차트 그리기
        df_cnt = df[col].value_counts()
        axs[0].pie(df_cnt, labels=df_cnt.index, autopct='%1.1f')
        sns.barplot(x=df_cnt.index, y=df_cnt.values, data=df, ax=axs[1])

        # 바차트에 숫자 추가
        for i, v in enumerate(df_cnt.index):
            axs[1].text(v, df_cnt.values[i], df_cnt.values[i],
                        fontsize=8,
                        horizontalalignment='center',
                        verticalalignment='bottom')

        axs[0].set_title(col + ' Pie Chart')
        axs[1].set_title(col + ' Bar Chart')

        fig.tight_layout()

    # 카디널리티가 큰 경우 (연속형에 가까운)
    else:
        fig, axs = plt.subplots(1, 2, figsize=(8, 4))

        # 박스플롯, 히스토그램 그리기
        sns.boxplot(x=col, data=df, orient='h', ax=axs[0])
        sns.histplot(x=col, data=df, bins=50, ax=axs[1])

        axs[0].set_title(col + ' Box Chart')
        axs[1].set_title(col + ' Hist Chart')

    plt.show()


def show_corr(df, x_col, y_col):
    x_crd = len(df[x_col].unique())
    y_crd = len(df[y_col].unique())
    crd_threshold = 20

    if x_crd < crd_threshold and y_crd < crd_threshold:
        pass

