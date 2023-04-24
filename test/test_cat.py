import pandas as pd
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding="utf-8")

path_data = config['DATA']['path_test_data']
path_result = config['DATA']['path_test_result']
df_orig = pd.read_csv(os.path.join(path_data, config['DATA']['name_train ']))
df_result = pd.read_csv(os.path.join(path_result, 'result.csv'))
#list_orig_cat = df_orig['Category'].unique()
class_names = ['business', 'tech', 'politics', 'sport', 'entertainment']
list_result_cat = df_result['labels'].unique()
def test_answer():
    assert set(class_names) == set(list_result_cat)
