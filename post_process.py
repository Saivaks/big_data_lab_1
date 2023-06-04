import pandas as pd
import kafka


def send_results(producer, topic, df):
    for index, row in df.iterrows():
        row = row.to_json().encode('utf-8')
        index = str(index).encode('utf-8')
        producer.send(topic, key=index, value=row)
    producer.flush()
    print("Данные успешно были отправлены в:", topic)

def get_results(consumer, topic):
    consumer.subscribe([topic])
    print("Запрос данных из:", topic)
    data = []
    columns = None
    while True:
        messages = consumer.poll(timeout_ms=1000, max_records=100)
        if not messages:
            break
        for _, msgs in messages.items():
            for message in msgs:
                index = int(message.key.decode('utf-8'))
                row = pd.read_json(message.value.decode('utf-8'), typ = 'series')
                if not columns:
                    columns = row.index.to_list()
                data.append((index, row))
    dataframe = None
    if columns:
        dataframe = pd.DataFrame.from_dict(dict(data), orient = 'index', columns = columns)
    return dataframe

def send_to_baza(consumer, topic, name_table, cursor):
	df = get_results(consumer, topic)
	#print(df)
	#df.to_sql(name_table, conn, schema = 'test', index=False, if_exists='replace')
	cursor.execute("TRUNCATE TABLE test.{}".format(name_table))
	cursor.commit()
	if name_table == 'train':
		for index, row in df.iterrows():
			cursor.execute("INSERT INTO test.train (ArticleId, Text, Category) values(?,?,?)", row.ArticleId, row.Text, row.Category)
	elif name_table == 'test':
		for index, row in df.iterrows():
			cursor.execute("INSERT INTO test.test (ArticleId, Text) values(?,?)", row.ArticleId, row.Text)
	elif name_table == 'train_split':
		for index, row in df.iterrows():
			cursor.execute("INSERT INTO test.train_split (ArticleId, Text, Category) values(?,?,?)", row.ArticleId, row.Text, row.Category)
	elif name_table == 'valid_split':
		for index, row in df.iterrows():
			cursor.execute("INSERT INTO test.valid_split (ArticleId, Text, Category) values(?,?,?)", row.ArticleId, row.Text, row.Category)
	elif name_table == 'pred_valid':
		for index, row in df.iterrows():
			cursor.execute("INSERT INTO test.pred_valid (Text, Category, Labels) values(?,?,?)", row.text, row.Category, row.labels)
	elif name_table == 'pred_test':
		for index, row in df.iterrows():
			cursor.execute("INSERT INTO test.pred_test (Text, Category) values(?,?)", row.text, row.labels)
	cursor.commit()
	print("Данные были успешно добавленны в таблицу:", name_table)