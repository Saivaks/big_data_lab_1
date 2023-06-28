from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import sklearn
from scipy.sparse import hstack
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import configparser
import pyodbc
import pymssql
import time
import socket
def procces():
	password = os.environ['PASSWORD']
	server = 'baza'
	db = os.environ['DB']
	user = os.environ['USER'] 
	port = os.environ['PORT']
	driver = r'/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so'
	#time.sleep(1000000000)
	time.sleep(10)
	#conn = pyodbc.connect(DRIVER='/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so', 
	#                   SERVER=server,
	#                   DATABASE=db,
	#                   UID=user,
	#                   PWD=password)
	print("Старт соеденения")
	#conn = pyodbc.connect(DRIVER = r'/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so', SERVER = 'baza', DATABASE = 'msdb', PORT = '1433', UID = 'sa', PWD = '12345And', TDS_Version = '7.2')
	conn = pyodbc.connect(DRIVER = driver, SERVER = server, DATABASE = db, PORT = port, UID = user, PWD = password)
	#print(password)
	#conn = pymssql.connect(server, user, password, db)
	cursor = conn.cursor()
	#cursor.execute('beton.sql')
	print("Создается схема с таблицами")
	with open(r'eto_baza/beton.sql') as f: 
			sql = f.read()
			#print(sql)
			cursor.execute(sql)
			cursor.commit()
	print("Создание завершенно")

	config = configparser.ConfigParser()
	config.read('config.ini', encoding="utf-8")

	#path_data = r'S:\andrey\мага\sem_2\big_data\big_data_lab_1\data'
	path_data = config['DATA']['path_data']
	#train = pd.read_csv(os.path.join(path_data, 'BBC News Train.csv'))
	#test = pd.read_csv(os.path.join(path_data, 'BBC News Test.csv'))
	train = pd.read_csv(os.path.join(path_data, config['DATA']['name_train']))
	#print(train)
	print("Запись обучающих данных в базу")
	cursor.execute("TRUNCATE TABLE test.train")
	cursor.commit()
	for index, row in train.iterrows():
		cursor.execute("INSERT INTO test.train (ArticleId, Text, Category) values(?,?,?)", row.ArticleId, row.Text, row.Category)
	cursor.commit()
	print("Запись тестовых данных в базу")
	test = pd.read_csv(os.path.join(path_data, config['DATA']['name_test']))
	cursor.execute("TRUNCATE TABLE test.test")
	cursor.commit()
	for index, row in test.iterrows():
		cursor.execute("INSERT INTO test.test (ArticleId, Text) values(?,?)", row.ArticleId, row.Text)
	cursor.commit()
	print("Завершение записи исходных данных")
	#test = pd.read_csv(os.path.join(path_data, config['DATA']['name_test']))
	train, valid = np.split(train.sample(frac=1, random_state=322), [int(float(config['SPLIT_DATA']['size'])*len(train))])
	
	print("Старт записи распличенных файлов")
	cursor.execute("TRUNCATE TABLE test.train_split")
	cursor.commit()
	for index, row in train.iterrows():
		cursor.execute("INSERT INTO test.train_split (ArticleId, Text, Category) values(?,?,?)", row.ArticleId, row.Text, row.Category)
	cursor.commit()	
	cursor.execute("TRUNCATE TABLE test.valid_split")
	cursor.commit()
	for index, row in valid.iterrows():
		cursor.execute("INSERT INTO test.valid_split (ArticleId, Text, Category) values(?,?,?)", row.ArticleId, row.Text, row.Category)
	cursor.commit()
	cursor.close()
	#train.to_csv('train.csv', index = False)
	#valid.to_csv('valid.csv', index = False)
	print("Процесс подготовки данных завершился")
#class_num = train['Category'].unique()
#class_names = {0:'business', 1:'tech', 2:'politics', 3:'sport', 4:'entertainment'}

#train_text = train['Text']
#valid_text = valid['Text']
#test_text = test['Text']

#all_text = pd.concat([train_text, valid_text, test_text])

