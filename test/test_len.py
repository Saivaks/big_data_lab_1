import pandas as pd
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding="utf-8")

path_data = config['DATA']['path_test_data']
path_result = config['DATA']['path_test_result']
df_orig = pd.read_csv(os.path.join(path_data, 'BBC News Test.csv'))
df_result = pd.read_csv(os.path.join(path_result, 'result.csv'))
def test_answer():
    assert len(df_orig) == len(df_result)

