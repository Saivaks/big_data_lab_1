#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from scipy.sparse import hstack

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[2]:


path_data = r'S:\andrey\мага\sem_2\big_data\big_data_lab_1\data'
train = pd.read_csv(os.path.join(path_data, 'BBC News Train.csv'))
test = pd.read_csv(os.path.join(path_data, 'BBC News Test.csv'))


# In[3]:


train['Category'].unique()


# In[4]:


class_names = {0:'business', 1:'tech', 2:'politics', 3:'sport', 4:'entertainment'}


# In[5]:


train_text = train['Text']
test_text = test['Text']
all_text = pd.concat([train_text, test_text])


# In[6]:


word_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    strip_accents='unicode',
    analyzer='word',
    #token_pattern=r\w{1,},
    stop_words='english',
    ngram_range=(1, 1),
    max_features=10000)
word_vectorizer.fit(all_text)


# In[7]:


train_word_features = word_vectorizer.transform(train_text)
test_word_features = word_vectorizer.transform(test_text)


# In[8]:


char_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    strip_accents='unicode',
    analyzer='char',
    #stop_words='english',
    ngram_range=(2, 6),
    max_features=50000)
char_vectorizer.fit(all_text)


# In[9]:


train_char_features = char_vectorizer.transform(train_text)
test_char_features = char_vectorizer.transform(test_text)


# In[10]:


train_features = hstack([train_char_features, train_word_features])
test_features = hstack([test_char_features, test_word_features])


# In[11]:


submission = pd.DataFrame.from_dict({'ArticleId': test['ArticleId']})
train_target = train['Category']
classifier = LogisticRegression(C=0.1, solver='sag')
#cv_score = np.mean(cross_val_score(classifier, train_features, train_target, cv=3, scoring='roc_auc'))
#scores.append(cv_score)
#print('CV score for class {} is {}'.format(class_name, cv_score))
classifier.fit(train_features, train_target)
result_train = classifier.predict_proba(train_features)
result = classifier.predict_proba(test_features)


# In[12]:


submission = []
for ind in range(len(result_train)):
    submission.append(list(result_train[ind]).index(max(result_train[ind])))


# In[13]:


some = list(train['Category'])
for ind in range(len(some)):
    some[ind] = list(filter(lambda x: class_names[x] == some[ind], class_names))[0]


# In[16]:


import sklearn
sklearn.metrics.precision_score(some, submission, average = 'micro')


# In[17]:


submission_test = []
for ind in range(len(result)):
    submission_test.append(list(result[ind]).index(max(result[ind])))


# In[23]:


some_test = []
for ind in range(6,8):
    #print('Текст:', test['Text'][ind], 'Категория:', class_names[submission_test[ind]])
    some_test.append(class_names[submission_test[ind]])


# In[ ]:




