from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import sklearn
from scipy.sparse import hstack
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import configparser
import pickle
import sparse
import pyodbc
def test():
    #config = configparser.ConfigParser()
    #config.read('config.ini', encoding="utf-8")
    #path_data = config['DATA']['path_data']
    #test = pd.read_csv(os.path.join(path_data, config['DATA']['name_test']))
    #train = pd.read_csv('train.csv')
    #valid = pd.read_csv('valid.csv')

    password = os.environ['PASSWORD']
    server = 'baza'
    db = 'msdb'
    user = 'SA'
    port = '1433'
    full = r'127.0.0.1::1433'
    driver = r'/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so'

    conn = pyodbc.connect(DRIVER = driver, SERVER = server, DATABASE = db, PORT = port, UID = user, PWD = password)
    cursor = conn.cursor()

    test = pd.read_sql("SELECT [ArticleId], [Text] FROM test.test;", conn)
    train = pd.read_sql("SELECT [ArticleId], [Text], [Category] FROM test.train_split;", conn)
    valid = pd.read_sql("SELECT [ArticleId], [Text], [Category] FROM test.valid_split;", conn)

    train_text = train['Text']
    valid_text = valid['Text']
    test_text = test['Text']
    train_target = train['Category']
    valid_target = valid['Category']
    class_names = {0:'business', 1:'tech', 2:'politics', 3:'sport', 4:'entertainment'}

    pkl_filename = "classifier.pkl"
    with open(pkl_filename, 'rb') as file:
        classifier = pickle.load(file)
    pkl_filename = "char_vectorizer.pkl"
    with open(pkl_filename, 'rb') as file:
        char_vectorizer = pickle.load(file)
    pkl_filename = "word_vectorizer.pkl"
    with open(pkl_filename, 'rb') as file:
        word_vectorizer = pickle.load(file)

    #train_char_features = sparse.load_npz("train_char_features.npz")
    #valid_char_features = sparse.load_npz("valid_char_features.npz")
    #test_char_features = sparse.load_npz("test_char_features.npz")

    #train_word_features = sparse.load_npz("train_word_features.npz")
    #valid_word_features = sparse.load_npz("valid_word_features.npz")
    #test_word_features = sparse.load_npz("test_word_features.npz")
    train_word_features = word_vectorizer.transform(train_text)
    valid_word_features = word_vectorizer.transform(valid_text)
    test_word_features = word_vectorizer.transform(test_text)

    train_char_features = char_vectorizer.transform(train_text)
    valid_char_features = char_vectorizer.transform(valid_text)
    test_char_features = char_vectorizer.transform(test_text)

    train_features = hstack([train_char_features, train_word_features])
    valid_features = hstack([valid_char_features, valid_word_features])
    test_features = hstack([test_char_features, test_word_features])

    result_train = classifier.predict_proba(train_features)
    result_valid = classifier.predict_proba(valid_features)
    result = classifier.predict_proba(test_features)


    submission = []
    for ind in range(len(result_train)):
        submission.append(list(result_train[ind]).index(max(result_train[ind])))
    some = list(train['Category'])
    for ind in range(len(some)):
        some[ind] = list(filter(lambda x: class_names[x] == some[ind], class_names))[0]
    acc = sklearn.metrics.precision_score(some, submission, average = 'micro')
    print("Точность на обучении:", acc)

    submission_valid = []
    for ind in range(len(result_valid)):
        submission_valid.append(list(result_valid[ind]).index(max(result_valid[ind])))
    some = list(valid['Category'])
    for ind in range(len(some)):
        some[ind] = list(filter(lambda x: class_names[x] == some[ind], class_names))[0]
    acc_v = sklearn.metrics.precision_score(some, submission_valid, average = 'micro')
    print("Точность на валидации:", acc_v)

    submission_valid = []
    for ind in range(len(result_valid)):
        index = list(result_valid[ind]).index(max(result_valid[ind]))
        submission_valid.append(class_names[index])
    valid_answer = {"text": list(valid['Text']),"Category":valid_target ,"labels": submission_valid}
    res = pd.DataFrame.from_dict(valid_answer)

    cursor.execute("TRUNCATE TABLE test.pred_valid")
    cursor.commit()
    for index, row in res.iterrows():
        cursor.execute("INSERT INTO test.pred_valid (Text, Category, Labels) values(?,?,?)", row.text, row.Category, row.labels)
    cursor.commit()
    #res.to_csv('result_valid.csv', index = False)

    submission_test = []
    for ind in range(len(result)):
        index = list(result[ind]).index(max(result[ind]))
        submission_test.append(class_names[index])
    test_answer = {"text": list(test['Text']), "labels": submission_test}
    res = pd.DataFrame.from_dict(test_answer)

    cursor.execute("TRUNCATE TABLE test.pred_test")
    cursor.commit()
    for index, row in res.iterrows():
        cursor.execute("INSERT INTO test.pred_test (Text, Category) values(?,?)", row.text, row.labels)
    cursor.commit()
    cursor.close()
    #res.to_csv('result.csv', index = False)
    print("Процесс тестирования модели завершился")