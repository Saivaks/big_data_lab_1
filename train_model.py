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
import pyodbc
from scipy import sparse
def train():
    password = os.environ['PASSWORD']
    server = 'baza'
    db = os.environ['DB']
    user = os.environ['USER'] 
    port = os.environ['PORT']
    driver = r'/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so'
    conn = pyodbc.connect(DRIVER = driver, SERVER = server, DATABASE = db, PORT = port, UID = user, PWD = password)
    cursor = conn.cursor()

    config = configparser.ConfigParser()
    config.read('config.ini', encoding="utf-8")
    #path_data = config['DATA']['path_data']
    #test = pd.read_csv(os.path.join(path_data, config['DATA']['name_test']))
    #train = pd.read_csv('train.csv')
    #valid = pd.read_csv('valid.csv')

    test = pd.read_sql("SELECT [ArticleId], [Text] FROM test.test;", conn)
    train = pd.read_sql("SELECT [ArticleId], [Text], [Category] FROM test.train_split;", conn)
    valid = pd.read_sql("SELECT [ArticleId], [Text], [Category] FROM test.valid_split;", conn)
    cursor.close()
    train_text = train['Text']
    valid_text = valid['Text']
    test_text = test['Text']
    all_text = pd.concat([train_text, valid_text, test_text])

    word_vectorizer = TfidfVectorizer(
        sublinear_tf=bool(config['word_vectorizer']['sublinear_tf']),
        strip_accents=str(config['word_vectorizer']['strip_accents']),
        analyzer=config['word_vectorizer']['analyzer'],
        stop_words=config['word_vectorizer']['stop_words'],
        ngram_range=(int(config['word_vectorizer']['ngram_range_min']), int(config['word_vectorizer']['ngram_range_max'])),
        max_features=int(config['word_vectorizer']['max_features']))
    word_vectorizer.fit(all_text)
    pkl_filename = "word_vectorizer.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(word_vectorizer, file)

    train_word_features = word_vectorizer.transform(train_text)
    valid_word_features = word_vectorizer.transform(valid_text)
    test_word_features = word_vectorizer.transform(test_text)

    char_vectorizer = TfidfVectorizer(
        sublinear_tf=bool(config['char_vectorizer']['sublinear_tf']),
        strip_accents=str(config['char_vectorizer']['strip_accents']),
        analyzer=config['char_vectorizer']['analyzer'],
        ngram_range=(int(config['char_vectorizer']['ngram_range_min']), int(config['char_vectorizer']['ngram_range_max'])),
        max_features=int(config['char_vectorizer']['max_features']))
    char_vectorizer.fit(all_text)
    pkl_filename = "char_vectorizer.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(char_vectorizer, file)
        
    train_char_features = char_vectorizer.transform(train_text)
    valid_char_features = char_vectorizer.transform(valid_text)
    test_char_features = char_vectorizer.transform(test_text)

    train_features = hstack([train_char_features, train_word_features])
    valid_features = hstack([valid_char_features, valid_word_features])
    test_features = hstack([test_char_features, test_word_features])


    train_target = train['Category']
    valid_target = valid['Category']

    classifier = LogisticRegression(C=float(config['LogisticRegression']['C']), solver=str(config['LogisticRegression']['solver']))
    classifier.fit(train_features, train_target)

    pkl_filename = "classifier.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(classifier, file)

    print("Процесс обучения модели завершился")
