# -*- coding: utf-8 -*-
"""new_category.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mLbt1tcqXoB3eG0V5VFdk0Pu0SK1qdz6
"""

import os
os.getcwd()

from google.colab import drive
drive.mount('/content/drive')

!pip install JPype1-1.1.2-cp36-cp36m-win_amd64.whl
!pip install nltk
!pip install tweepy
!pip install konlpy
!pip install tensorflow

from sklearn.datasets import load_files
from bs4 import BeautifulSoup
import re
import konlpy
import pandas as pd
import nltk
import tensorflow as tf
tf.random.set_seed(777) #하이퍼파라미터 튜닝을 위해 실행시 마다 변수가 같은 초기값 가지게 하기
from sklearn.model_selection import train_test_split
import numpy as np

from keras import optimizers

def clean_korean_documents(documents):
    # #텍스트 정제 (HTML 태그 제거)
    # for i, document in enumerate(documents):
    #     document = BeautifulSoup(document, 'html.parser').text 
    #     documents[i] = document

    #텍스트 정제 (특수기호 제거)
    for i, document in enumerate(documents):
        document = re.sub(r'[^ ㄱ-ㅣ가-힣]', '', document) #특수기호 제거, 정규 표현식
        documents[i] = document

    #텍스트 정제 (형태소 분석)
    for i, document in enumerate(documents):
        okt = konlpy.tag.Okt()
        clean_words = []
        for word in okt.pos(document, stem=True): #어간 추출
            if word[1] in ['Noun', 'Verb', 'Adjective']: #명사, 동사, 형용사
                clean_words.append(word[0])
        document = ' '.join(clean_words)
        documents[i] = document

    #텍스트 정제 (불용어 제거)
    df = pd.read_csv('https://raw.githubusercontent.com/cranberryai/todak_todak_python/master/machine_learning_text/clean_korean_documents/korean_stopwords.txt', header=None)
    df[0] = df[0].apply(lambda x: x.strip())
    stopwords = df[0].to_numpy()
    # nltk.download('punkt')
    for i, document in enumerate(documents):
        clean_words = [] 
        for word in nltk.tokenize.word_tokenize(document): 
            if word not in stopwords: #불용어 제거
                clean_words.append(word)
        documents[i] = ' '.join(clean_words)  

    return documents

##########데이터 로드
df = pd.read_csv('/content/cate.csv',encoding='cp949')
df.loc[(df['cate'] == "경제"), 'cate'] = 0
df.loc[(df['cate'] == "국제"), 'cate'] = 0
df.loc[(df['cate'] == "문화"), 'cate'] = 1 
df.loc[(df['cate'] == "사회"), 'cate'] = 0  
df.loc[(df['cate'] == "스포츠"), 'cate'] = 2  
df.loc[(df['cate'] == "정치"), 'cate'] = 0 
df.loc[(df['cate'] == "IT_과학"), 'cate'] = 1 
labels = ['일반', '연예/과학', '스포츠']

##########데이터 분석

##########데이터 전처리
x_data=df.title
y_data=df.cate
y_data=pd.to_numeric(y_data)
x_data = clean_korean_documents(x_data) #텍스트 정제
tokenizer_cate = tf.keras.preprocessing.text.Tokenizer() 
tokenizer_cate.fit_on_texts(x_data)
x_data = tokenizer_cate.texts_to_sequences(x_data) #정수 인코딩
sequence_length = 100
x_data = tf.keras.preprocessing.sequence.pad_sequences(x_data, maxlen=sequence_length)

y_data = tf.keras.utils.to_categorical(y_data)

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.25, random_state=7, stratify=y_data)

##########모델 생성

input = tf.keras.layers.Input(shape=(sequence_length,))
net = tf.keras.layers.Dense(units=27, activation='relu')(input)
net = tf.keras.layers.Dense(units=27, activation='relu')(net)
net = tf.keras.layers.Dense(units=3, activation='softmax')(net)
cate = tf.keras.models.Model(input, net)

##########모델 학습
Adam = tf.keras.optimizers.Adam(
learning_rate=0.007, beta_1=0.9, beta_2=0.999, epsilon=5e-05, amsgrad=False,
name='Adam'
)
cate.compile( optimizer=Adam, loss='categorical_crossentropy', metrics=['accuracy'])

cate.fit(x_train, y_train, epochs=50, validation_data=(x_test, y_test)) 

##########모델 검증

##########모델 예측

def cat_pred(sen) :

  x_test = np.array([
      sen  #"박나래, 생애 첫 MC였던 ‘비디오스타’ 막방에 눈물…잠시만 안녕"
  ])
  x_test = clean_korean_documents(x_test) #텍스트 정제
  x_test = tokenizer_cate.texts_to_sequences(x_test) #정수 인코딩
  x_test = tf.keras.preprocessing.sequence.pad_sequences(x_test, maxlen=sequence_length) #길이 맞추기

  y_predict = cate.predict(x_test)
  print(y_predict[0])
  label = labels[y_predict[0].argmax()]
  confidence = y_predict[0][y_predict[0].argmax()]
  print(label, confidence) 
  return label

test = """
"박나래, 생애 첫 MC였던 ‘비디오스타’ 막방에 눈물…잠시만 안녕"
"""
cat_pred(test)

