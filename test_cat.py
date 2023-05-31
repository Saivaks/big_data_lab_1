import pandas as pd
import os
import configparser
import os
import pyodbc
def test1():
    password = os.environ['PASSWORD']
    server = 'baza'
    db = 'msdb'
    user = 'SA'
    port = '1433'
    full = r'127.0.0.1::1433'
    driver = r'/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so'
    conn = pyodbc.connect(DRIVER = driver, SERVER = server, DATABASE = db, PORT = port, UID = user, PWD = password)
    cursor = conn.cursor()
    df_result = pd.read_sql("SELECT [Text],  [Category], [Labels] FROM test.pred_valid;", conn)
    cursor.close()
    class_names = ['business', 'tech', 'politics', 'sport', 'entertainment']
    list_result_cat = df_result['Labels'].unique()
    print("Старт 1 теста")
    def test_answer():
        assert set(class_names) == set(list_result_cat)
