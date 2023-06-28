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
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
import confluent_kafka.admin, pprint
import post_process
import kafka
import sqlalchemy as sa
import urllib

def procces():
	password = os.environ['PASSWORD']
	server = 'baza'
	db = os.environ['DB']
	user = os.environ['USER'] 
	port = os.environ['PORT']
	driver = r'/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so'
	server_kafka = 'kafka:29092'

	print("Старт соеденения")
	#conn = pyodbc.connect(DRIVER = r'/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so', SERVER = 'baza', DATABASE = 'msdb', PORT = '1433', UID = 'sa', PWD = '12345And', TDS_Version = '7.2')
	conn = pyodbc.connect(DRIVER = driver, SERVER = str(server), DATABASE = str(db), PORT = str(port), UID = str(user), PWD = str(password))
	#print(password)
	#conn = pymssql.connect(server, user, password, db)
	cursor = conn.cursor()
	#cursor.execute('beton.sql')

	config = configparser.ConfigParser()
	config.read('config.ini', encoding="utf-8")

	#path_data = r'S:\andrey\мага\sem_2\big_data\big_data_lab_1\data'
	path_data = config['DATA']['path_data']
	#train = pd.read_csv(os.path.join(path_data, 'BBC News Train.csv'))
	#test = pd.read_csv(os.path.join(path_data, 'BBC News Test.csv'))
	train = pd.read_csv(os.path.join(path_data, config['DATA']['name_train']))
	#print(train)
	print("Запись обучающих данных в кафку")
	client = KafkaProducer(bootstrap_servers = server_kafka, api_version=(0, 10, 1))
	name_topic = 'train'
	post_process.send_results(client, name_topic, train)

	#cursor.execute("TRUNCATE TABLE test.train")
	#cursor.commit()
	#for index, row in train.iterrows():
	#	cursor.execute("INSERT INTO test.train (ArticleId, Text, Category) values(?,?,?)", row.ArticleId, row.Text, row.Category)
	#cursor.commit()
	print("Запись тестовых данных в кафку")
	test = pd.read_csv(os.path.join(path_data, config['DATA']['name_test']))
	name_topic = 'test'
	post_process.send_results(server_kafka, name_topic, test)

	train, valid = np.split(train.sample(frac=1, random_state=322), [int(float(config['SPLIT_DATA']['size'])*len(train))])
	print("Старт записи распличенных файлов в кафку")
	name_topic = 'train_split'
	post_process.send_results(server_kafka, name_topic, train)

	name_topic = 'valid_split'
	post_process.send_results(server_kafka, name_topic, valid)
	


	print("Запись данных в базу")
	#conn_eng = urllib.parse.quote_plus('DRIVER='+driver+';SERVER='+server+';PORT='+port+';DATABASE='+db+';UID='+user+';PWD='+ password)
	#engine = sa.create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn_eng))
	consumer = kafka.KafkaConsumer(bootstrap_servers = server_kafka, auto_offset_reset = 'earliest')

	post_process.send_to_baza(consumer, 'train', 'train', cursor)
	post_process.send_to_baza(consumer, 'test', 'test', cursor)
	post_process.send_to_baza(consumer, 'train_split', 'train_split', cursor)
	post_process.send_to_baza(consumer, 'valid_split', 'valid_split', cursor)
	cursor.commit()
	cursor.close()
	#train.to_csv('train.csv', index = False)
	#valid.to_csv('valid.csv', index = False)
	print("Процесс подготовки данных завершился")
	#time.sleep(1000000000)
#class_num = train['Category'].unique()
#class_names = {0:'business', 1:'tech', 2:'politics', 3:'sport', 4:'entertainment'}

#train_text = train['Text']
#valid_text = valid['Text']
#test_text = test['Text']

#all_text = pd.concat([train_text, valid_text, test_text])

