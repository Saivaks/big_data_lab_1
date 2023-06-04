import pyodbc
from kafka.admin import KafkaAdminClient, NewTopic
import confluent_kafka.admin, pprint
import os
import time

def create_env():
	password = os.environ['PASSWORD']
	server = 'baza'
	db = os.environ['DB']
	user = os.environ['USER'] 
	port = os.environ['PORT']
	driver = r'/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so'
	server_kafka = 'kafka:29092'
	time.sleep(10)
	print("Старт соеденения")
	conn = pyodbc.connect(DRIVER = driver, SERVER = server, DATABASE = db, PORT = port, UID = user, PWD = password)
	cursor = conn.cursor()
	print("Создается схема с таблицами")
	with open('beton.sql') as f: 
		sql = f.read()
		cursor.execute(sql)
		cursor.commit()
	print("Создание завершенно базы завершенно")

	conf = {'bootstrap.servers': server_kafka}
	kafka_admin = confluent_kafka.admin.AdminClient(conf)
	new_topic = []
	new_topic.append(confluent_kafka.admin.NewTopic('train', 1, 1))
	new_topic.append(confluent_kafka.admin.NewTopic('test', 1, 1))
	new_topic.append(confluent_kafka.admin.NewTopic('train_split', 1, 1))
	new_topic.append(confluent_kafka.admin.NewTopic('valid_split', 1, 1))
	new_topic.append(confluent_kafka.admin.NewTopic('pred_train', 1, 1))
	new_topic.append(confluent_kafka.admin.NewTopic('pred_valid', 1, 1))
	new_topic.append(confluent_kafka.admin.NewTopic('pred_test', 1, 1))
	kafka_admin.create_topics(new_topic)
	print("Доступные для записи топики:", kafka_admin.list_topics().topics)