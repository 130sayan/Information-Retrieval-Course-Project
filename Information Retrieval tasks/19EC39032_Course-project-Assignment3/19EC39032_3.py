from bs4 import BeautifulSoup
import re
import sys
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from datetime import datetime
from dateutil.parser import parse
import json
import os
import io
import numpy as np
from collections import Counter
from math import log10
import pickle
from numpy import linalg as LA
import itertools
import string
# import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestCentroid,KNeighborsClassifier
from sklearn import pipeline,ensemble,preprocessing,feature_extraction
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import f1_score
lemma=WordNetLemmatizer()
docid1=0
def tokenize(text):
          sofwords=word_tokenize(text)
          t1=str.maketrans('','','\t')
          #words=[word.translate(t1) for word in words]
          i=0;
          for word in sofwords:
              sofwords[i]=word.translate(t1)
              i=i+1
          pun=(string.punctuation).replace("'","")
          t_table=str.maketrans('','',pun)
          #strip_words=[word.translate(t_table) for word in sofwords]
          strip_words=[]
          i=0;
          for word in sofwords:
              strip_words.append(word.translate(t_table))
              i=i+1
          sofwords = [str for str in strip_words if str]
          #sofwords =[word.lower() for word in sofwords] 
          i=0;
          for word in sofwords:
              sofwords[i]=word.lower()
              i=i+1
          stop_words=set(stopwords.words('english'))
          #sofwords=[w for w in sofwords if w not in stop_words]
          i=0
          arr=[]
          for w in sofwords:
              if(w not in stop_words):
                  arr.append(w)
                  i=i+1
          sofwords=arr
          #words=[lemma.lemmatize(w) for w in words]
          i=0;
          for w in sofwords:
              # w=w.lower()
              sofwords[i]=lemma.lemmatize(w)
              # sofwords[i]=sofwords[i].lower()
              i=i+1
          return sofwords
# min_df=5,max_df=0.8,
docid2=1

def writeknn(i,listtrain,Ytrain,listtest,Ytest,fw3):
      pipe4=pipeline.Pipeline([('tfidf_vectorizer',TfidfVectorizer(tokenizer=tokenize,lowercase=True)),
      ('kNN_classifier',KNeighborsClassifier(n_neighbors=i)) ])
      pipe4.fit(listtrain,Ytrain)
      knn=pipe4.predict(listtest)
      stri=str(f1_score(knn,Ytest,average='macro'))
      fw3.write(stri+" ")
      

mainfolder=os.getcwd()
D1train=mainfolder+"/dataset/class1/train"
D1test=mainfolder+"/dataset/class1/test"
D2train=mainfolder+"/dataset/class2/train"
D2test=mainfolder+"/dataset/class2/test"
# os.chdir(D1train)
# lot=os.listdir(os.getcwd())
fileno=0
n=0
# df={}
# tf={}
# idf={}
lemma=WordNetLemmatizer()
docll=0

list1train=[]
os.chdir(D1train)
lot=os.listdir(os.getcwd())
while docid1<docid2:
    for fi in lot:
        file=io.open(fi,'r',encoding="utf-8",errors='ignore')
        etext = file.read()
        list1train.append(etext)
    docid1=docid1+1
    
list1test=[]
os.chdir(D1test)
lot=os.listdir(os.getcwd())
while docid1<=docid2:
    for fi in lot:
        file=io.open(fi,'r',encoding="utf-8",errors='ignore')
        etext = file.read()
        list1test.append(etext)
    docid1=docid1+1
    
list2train=[]
os.chdir(D2train)
lot=os.listdir(os.getcwd())
while docll<docid2:
    for fi in lot:
        file=io.open(fi,'r',encoding="utf-8",errors='ignore')
        etext = file.read()
        list2train.append(etext)
    docll=docll+1

list2test=[]
os.chdir(D2test)
lot=os.listdir(os.getcwd())
while docll<=docid2:
    for fi in lot:
        file=io.open(fi,'r',encoding="utf-8",errors='ignore')
        etext = file.read()
        list2test.append(etext)
    docll=docll+1

listtrain=list1train+list2train
listtest=list1test+list2test

A=np.zeros(len(list1train))
B=np.ones(len(list2train))
# Ytrain=np.concatenate(np.array(A),np.array(B))
Ytrain=np.concatenate((np.zeros(len(list1train)),np.ones(len(list2train))))

A=np.zeros(len(list1test))
B=np.ones(len(list2test))
# Ytest=np.concatenate(np.array(A),np.array(B))
Ytest=np.concatenate((np.zeros(len(list1test)),np.ones(len(list2test))))

os.chdir(mainfolder)


fw3=open('Results 3.txt',"w",encoding="utf-8")
fw3.write("NumFeature ")
for i in [1,10,50]:
    fw3.write(str(i))
    fw3.write(" ")
fw3.write("\n")
fw3.write("KNN ")
for i in [1,10,50]:
  writeknn(i,listtrain,Ytrain,listtest,Ytest,fw3)
fw3.write("\n")
fw3.close()
