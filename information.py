import pandas as pd


class Information:
    def __init__(self):
       pass

    def print_basic_data_info(self, data):
        """
        :param data: data, DataFrame
        :return: None
        """
        print(data.shape, end='\n\n')
        print(data.info(), end='\n\n')
        print('Data Sample (head) \n', data.head(), end='\n\n')
        print('Data Sample (tail) \n', data.tail(), end='\n\n')
        print('Data Null Sum \n', data.isnull().sum(), end='\n\n')

