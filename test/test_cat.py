import pandas as pd
import os
path_data = r'S:\andrey\мага\sem_2\big_data\big_data_lab_1\data'
path_result = r'S:\andrey\мага\sem_2\big_data\big_data_lab_1'
df_orig = pd.read_csv(os.path.join(path_data, 'BBC News Test.csv'))
df_result = pd.read_csv(os.path.join(path_result, 'result.csv'))
#list_orig_cat = df_orig['Category'].unique()
class_names = ['business', 'tech', 'politics', 'sport', 'entertainment']
list_result_cat = df_result['labels'].unique()
def test_answer():
    assert set(class_names) == set(list_result_cat)
