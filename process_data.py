from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import sklearn
from scipy.sparse import hstack
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import configparser


config = configparser.ConfigParser()
config.read('config.ini', encoding="utf-8")

#path_data = r'S:\andrey\мага\sem_2\big_data\big_data_lab_1\data'
path_data = config['DATA']['path_data']
#train = pd.read_csv(os.path.join(path_data, 'BBC News Train.csv'))
#test = pd.read_csv(os.path.join(path_data, 'BBC News Test.csv'))
train = pd.read_csv(os.path.join(path_data, config['DATA']['name_train']))
#test = pd.read_csv(os.path.join(path_data, config['DATA']['name_test']))
train, valid = np.split(train.sample(frac=1, random_state=322), [int(float(config['SPLIT_DATA']['size'])*len(train))])

train.to_csv('train.csv', index = False)
valid.to_csv('valid.csv', index = False)
print("Процесс подготовки данных завершился")
#class_num = train['Category'].unique()
#class_names = {0:'business', 1:'tech', 2:'politics', 3:'sport', 4:'entertainment'}

#train_text = train['Text']
#valid_text = valid['Text']
#test_text = test['Text']

#all_text = pd.concat([train_text, valid_text, test_text])

