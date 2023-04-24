import pandas as pd
import os
path_data = r'S:\andrey\мага\sem_2\big_data\big_data_lab_1\data'
path_result = r'S:\andrey\мага\sem_2\big_data\big_data_lab_1'
df_orig = pd.read_csv(os.path.join(path_data, 'BBC News Test.csv'))
df_result = pd.read_csv(os.path.join(path_result, 'result.csv'))
def test_answer():
    assert len(df_orig) == len(df_result)

