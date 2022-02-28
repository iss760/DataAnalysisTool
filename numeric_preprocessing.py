import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler


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


# 이상치를 제거해주는 함수
def remove_outlier(df, cols, how='iqr'):
    """
    :param df: (DataFrame) 이상치를 제거할 데이터
    :param cols: (list[str] or str) 이상치를 제거할 데이터의 컬럼들
    :param how: 이상치 제거 방법
    :return: (DataFrame) 이상치가 제거된 데이터
    """
    _df = df.copy()
    cols = [cols] if type(cols) == str else cols  # 입력값 str 경우 처리

    # 입력값 예외처리
    if type(cols) != list:
        raise ValueError('Wrong input data type')

    # 제거할 이상치의 인덱스 리스트 생성
    rm_idx = []
    for col in cols:
        # iqr 방식
        if how == 'iqr':
            iqr_dict = _get_iqr(_df[col])
            rm_idx.extend(_df[_df[col] < iqr_dict['min']].index.tolist())
            rm_idx.extend(_df[_df[col] > iqr_dict['max']].index.tolist())
        # z-score 방식
        elif how == 'z':
            mean = np.mean(_df[col])
            std = np.std(_df[col])
            _df_z = _df[col].apply(lambda x: (x - mean) / std)
            rm_idx.extend(_df_z[_df_z > 3].index.tolist())
            rm_idx.extend(_df_z[_df_z > 3].index.tolist())
        # 잘못된 제거 알고리즘 선택
        else:
            raise ValueError('Incorrect algorithm selection')

    # 이상치 제거
    _df.drop(list(set(rm_idx)), inplace=True)

    return _df


def convert_outlier(df, cols, how='min-max'):
    _df = df.copy()
    cols = [cols] if type(cols) == str else cols    # 입력값 str 경우 처리

    # 입력값 예외처리
    if type(cols) != list:
        raise ValueError('Wrong input data type')
    '''
    미완성
    '''


# 데이터를 스케일링 해주는 함수
def scaling(df, cols, how='min-max'):
    """
    :param df: (DataFrame) 스케일링 할 데이터
    :param cols: (list[str]) 스케일링 할 데이터의 칼럼들
    :param how: (str) 스케일링 방법 선택
    :return: (DataFrame or Series) 스케일링된 데이터
    """
    if how == 'min-max':
        scaler = MinMaxScaler()
    elif how == 'robust':
        scaler = RobustScaler()
    elif how == 'standard':
        scaler = StandardScaler()
    else:
        raise ValueError('Wrong input data type')

    return scaler.fit_transform(df[cols])
