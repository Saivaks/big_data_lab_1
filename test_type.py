import pandas as pd
import os
import configparser
import pyodbc
def test3():
    password = os.environ['PASSWORD']
    server = 'baza'
    db = 'msdb'
    user = 'SA'
    port = '1433'
    full = r'127.0.0.1::1433'
    driver = r'/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so'

    conn = pyodbc.connect(DRIVER = driver, SERVER = server, DATABASE = db, PORT = port, UID = user, PWD = password)
    cursor = conn.cursor()

    df_orig = pd.read_sql("SELECT [Text] FROM test.test;", conn)
    df_result = pd.read_sql("SELECT [Text] FROM test.pred_test;", conn)
    cursor.close()
    print("Старт 3 теста")
    def test_answer():
        assert df_orig['Text'].dtypes == df_result['text'].dtypes 