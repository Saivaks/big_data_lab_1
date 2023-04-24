
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
test = pd.read_csv(os.path.join(path_data, config['DATA']['name_test']))
train, valid = np.split(train.sample(frac=1, random_state=322), [int(float(config['SPLIT_DATA']['size'])*len(train))])

#class_num = train['Category'].unique()
class_names = {0:'business', 1:'tech', 2:'politics', 3:'sport', 4:'entertainment'}

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

train_char_features = char_vectorizer.transform(train_text)
valid_char_features = char_vectorizer.transform(valid_text)
test_char_features = char_vectorizer.transform(test_text)

train_features = hstack([train_char_features, train_word_features])
valid_features = hstack([valid_char_features, valid_word_features])
test_features = hstack([test_char_features, test_word_features])

submission = pd.DataFrame.from_dict({'ArticleId': test['ArticleId']})
train_target = train['Category']
valid_target = valid['Category']

classifier = LogisticRegression(C=float(config['LogisticRegression']['C']), solver=str(config['LogisticRegression']['solver']))
classifier.fit(train_features, train_target)
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
res.to_csv('result_valid.csv', index = False)

submission_test = []
for ind in range(len(result)):
    index = list(result[ind]).index(max(result[ind]))
    submission_test.append(class_names[index])
test_answer = {"text": list(test['Text']), "labels": submission_test}
res = pd.DataFrame.from_dict(test_answer)
res.to_csv('result.csv', index = False)
#some_test = []
#for ind in range(6,8):
    #print('Текст:', test['Text'][ind], 'Категория:', class_names[submission_test[ind]])
#    some_test.append(class_names[submission_test[ind]])




