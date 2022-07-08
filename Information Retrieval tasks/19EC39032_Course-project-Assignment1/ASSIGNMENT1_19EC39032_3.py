

import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer
import json
import string
import os
import io
fno=0
lemma=WordNetLemmatizer()
mainD=os.getcwd()
D=mainD+"/ECTText"
os.chdir(D)
lof=os.listdir(os.getcwd())
poslist={}
for fi in lof:
     file=io.open(fi,encoding="utf-8")
     fr=file.read()
     print(fi)
     sofwords=word_tokenize(fr)
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
     for pos,term in enumerate(sofwords):
         if term not in poslist:
            poslist[term]=[]
            poslist[term].append(0)
            poslist[term][0]+=1
            poslist[term].append({})
            poslist[term][1][fno]=[pos]
         else:
            poslist[term][0]+=1
            if fno in poslist[term][1]:
                poslist[term][1][fno].append(pos)
            else:
                poslist[term][1][fno]=[pos]
     fno=fno+1
D2=mainD
os.chdir(D2)
pl=open("postinglist.json","w")
json.dump(poslist,pl)
pl.close()
