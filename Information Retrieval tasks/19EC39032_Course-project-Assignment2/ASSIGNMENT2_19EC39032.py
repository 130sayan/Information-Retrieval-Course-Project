

from bs4 import BeautifulSoup
import re
import sys
# import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
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
def writefunc(score_1,score_2,score_3,score_4,fR):
    flag=0
    count=1
    for i in score_1:
       # if flag==1:
       #   fR.write(",<"+str(i)+","+str(score_1[i])+">")
       s=str(i)
       s=s[:-4]
       if flag==0:
         fR.write("<"+s+","+str(score_1[i])+">")
         flag=1
         # print("YES")
         continue
       if flag==1:
         fR.write(",<"+s+","+str(score_1[i])+">")
       count=count+1
       if(count==10):
           break
    fR.write("\n")
    count=1
    flag=0
    for i in score_2:
       # if flag==1:
       #   fR.write(",<"+str(i)+","+str(score_2[i])+">")
       s=str(i)
       s=s[:-4]
       if flag==0:
         fR.write("<"+s+","+str(score_2[i])+">")
         flag=1
         continue
       if flag==1:
         fR.write(",<"+s+","+str(score_2[i])+">")
       count=count+1
       if(count==10):
           break
    fR.write("\n")
    count=1
    flag=0
    for i in score_3:
       # if flag==1:
       #   fR.write(",<"+str(i)+","+str(score_3[i])+">")
       s=str(i)
       s=s[:-4]
       if flag==0:
         fR.write("<"+s+","+str(score_3[i])+">")
         flag=1
         continue
       if flag==1:
         fR.write(",<"+s+","+str(score_3[i])+">")
       count=count+1
       if(count==10):
           break
    fR.write("\n")
    count=1
    flag=0
    for i in score_4:
       # if flag==1:
       #   fR.write(",<"+str(i)+","+str(score_4[i])+">")
       s=str(i)
       s=s[:-4]
       if flag==0:
         fR.write("<"+s+","+str(score_4[i])+">")
         flag=1
         continue
       if flag==1:
         fR.write(",<"+s+","+str(score_4[i])+">")
       count=count+1
       if(count==10):
           break
    fR.write("\n")
    fR.write("\n")
h=0
mainfolder=os.getcwd()
D2=mainfolder+"/Dataset/Dataset"
# D3=mainfolder+"/ECTNestedDict"
# if(os.path.isdir(D3)==False):
    # os.mkdir(D3)
D4=mainfolder+"/ECTText"
if(os.path.isdir(D4)==False):
    os.mkdir(D4)
os.chdir(D2)
lof=os.listdir(os.getcwd())
lof=sorted(lof)
for fi in lof:
    file=io.open(fi,encoding="utf-8")
    # print(fi)
    file_name=fi.strip()
    zl=0
    for zz in file_name:
        if(zz=='.'):
            break
        zl=zl+1
    file_name=file_name[:zl]
    # print(file_name)
    soup = BeautifulSoup(file, 'html.parser')
    pcount=soup.find_all(class_="p_count")
    nopara=len(pcount)+1
    #print(nopara)
    p1=soup.find_all(class_="p p1")
    s=p1[0].get_text()
    #print (len(p1))
    #print (len(s))
    s=s.strip()
    op=len(s)-1
    opc=0
    while(op>=0):
        if(s[op]==' ' and (s[op-1]!=' ' and op!=0)):
            opc=opc+1
        if(opc==6):
            break
        op=op-1
    s=s[op+1:]
    # result=parse(s,fuzzy_with_tokens=True)
    # date=result[0].strftime('%Y-%m-%d')
    s=s.strip()
    date=s
    #print(date)
    Participants=[]
    Participants.append("Operator")
    Roles=[]
    stemp="Conference Call Participants"
    i=2
    string=p1[i].get_text()
    #print(stemp.lower())
    string=string.strip()
    #if(p1[3].get_text()==stemp):
     #   print ("YES")
    while (1):
        if(string in Participants):
            break
        if(string.lower() == stemp.lower()):
            i=i+1
            #print(i)
            string=p1[i].get_text()
            string=string.strip()
            continue
        flag=1
        s1=" "
        s2=" "
        count=0
        ch=0
        for c in string:
            if(c==' ' and string[ch+1]!=' '):
                count+=1
            if ((c=='-' or count==2) and flag==1) :
                s1=s1.strip()
                flag=0
                Participants.append(s1)
            s1=s1+c
            if(flag==0):
                s2=s2+c
            ch=ch+1
        s2=s2.strip()
        Roles.append(s2)
        #Participants.append(string)
        i=i+1
        #print(i)
        if(i>=len(p1)):
            break
        string=p1[i].get_text()
        string=string.strip()
        #print(string.lower())
    #print(*Participants, sep = "\n")
    while(0):
        if(string in Participants):
            break
        Participants.append(p1[i].get_text())
        i=i+1
        #print(i)
        string=p1[i].get_text()
        string=string.strip()
    #print(*Participants, sep = "\n")
    #print(*Roles, sep = "\n")
    Presentation={}
    #Presentation['Participants']=[]
    flag=0
    stemp="Question-and-Answer Session"
    j=i;
    while(j<len(p1)):
        string=p1[j].get_text()
        string=string.strip()
        if(string==stemp):
            j=j+1
            flag=1
            break
        if(string in Participants):
            j=j+1
            if(j==len(p1)):
                if(string in Presentation):
                    string=string
                else:
                    Presentation[string]=[]
                break
            val=p1[j].get_text()
            val=val.strip()
            if(string in Presentation):
                string=string
            else:
                Presentation[string]=[]
            while(1):
                if(val.lower() == stemp.lower()):
                    flag=1
                    break
                if(val in Participants):
                    j=j-1
                    break
                Presentation[string].append(val)
                j=j+1
                if(j==len(p1)):
                    break
                val=p1[j].get_text()
                val=val.strip()
        j=j+1
        if(flag==1):
            break
    #print(*Presentation, sep = " ")
    count_sven = 0
    Questionnaire={}
    i=0
    k=j
    azp = 1
    if(flag==1):
        while(k<len(p1)):
            i=i+1
            Questionnaire[i]={}
            string=p1[k].get_text()
            string=string.strip()
            #print(string+"\n")
            #print(k)
            if((string in Participants) or ((string.startswith("Q -")) or (string.startswith("A -")))):
                #print(string+"\n")
                Questionnaire[i]["Speaker"]=string
                Questionnaire[i]["Remark"]=[]
                k=k+1
                #print(k)
                if(k==len(p1)):
                    break
                val=p1[k].get_text()
                val=val.strip()
                #print(val+"\n")
                while(1):
                    if(val in Participants):
                        k=k-1
                        break
                    Questionnaire[i]["Remark"].append(val)
                    #print(val+"\n")
                    k=k+1
                    if(k==len(p1)):
                        break
                    val=p1[k].get_text()
                    val=val.strip()
            k=k+1
    #print(*Questionnaire[2]["Remark"], sep = " ")
    for n in range(2,nopara+1):
        p1=soup.find_all(class_="p p%d"%n)
        j=0
        if(flag==0):
            stemp="Question-and-Answer Session"
            j=0
            while(j<len(p1)):
                s=p1[j].get_text()
                s=s.strip()
                if(s==stemp):
                    j=j+1
                    flag=1
                    break
                if(s in Participants):
                    string=s
                    j=j+1
                    if(j==len(p1)):
                        if(string in Presentation):
                            string=string
                        else:
                            Presentation[string]=[]
                        break
                    val=p1[j].get_text()
                    val=val.strip()
                    if(string in Presentation):
                        string=string
                    else:
                        Presentation[string]=[]
                    while(1):
                        if(val.lower() == stemp.lower()):
                            flag=1
                            break
                        if(val in Participants):
                            j=j-1
                            break
                        Presentation[string].append(val)
                        j=j+1
                        if(j==len(p1)):
                            break
                        val=p1[j].get_text()
                        val=val.strip()
                else:
                    if(string not in Presentation):
                        Presentation[string]=[]
                    Presentation[string].append(s)
                j=j+1
                if(flag==1):
                    break
        if(flag==1):
            k=j
            while(k<len(p1)):
                s=p1[k].get_text()
                s=s.strip()
                #print(string+"\n")
                #print(k)
                if((s in Participants) or (s.startswith("Q -"))):
                    i=i+1
                    Questionnaire[i]={}
                    string=s
                    #print(string+"\n")
                    Questionnaire[i]["Speaker"]=string
                    Questionnaire[i]["Remark"]=[]
                    k=k+1
                    #print(k)
                    if(k==len(p1)):
                        break
                    val=p1[k].get_text()
                    val=val.strip()
                    #print(val+"\n")
                    while(1):
                        if(val in Participants):
                            k=k-1
                            break
                        Questionnaire[i]["Remark"].append(val)
                        #print(val+"\n")
                        k=k+1
                        if(k==len(p1)):
                            break
                        val=p1[k].get_text()
                        val=val.strip()
                else:
                    if(i==0):
                        break
                    Questionnaire[i]["Remark"].append(s)
                k=k+1
    #print(*Questionnaire[2]["Speaker"])
    Dictionary={}
    Dictionary['date']=date
    Dictionary['participants']=Participants
    Dictionary['presentation']=Presentation
    Dictionary['questionnaire']=Questionnaire
    #print(*Dictionary['questionnaire'][2]["Speaker"])
    # D3=mainfolder+"/ECTNestedDict"
    # os.chdir(D3)
    # dic1=open("Dic%d.json"%h,"w")
    # json.dump(Dictionary,dic1)
    # dic1.close()
    # D4=mainfolder+"/ECTText"
    os.chdir(D4)
    f=open(file_name+".txt","w+",encoding='utf-8')
    f.write("Date-\n\n")
    f.write(Dictionary['date']+"\n\n")
    f.write("Participants-\n\n")
    r=0
    for p in Dictionary['participants']:
            f.write(p+" ")
            if(r!=0):
                f.write(Roles[r-1])
            f.write("\n")
            r=r+1
    f.write("\nPresentation-\n")
    for p in Dictionary['presentation']:
            f.write("\n"+p+"\n")
            for v in Dictionary['presentation'][p]:
              f.write(v+"\n")
    f.write("\nQuestionnaire-\n")
    for p in Dictionary['questionnaire']:
            f.write("\n%d. "%p)
            f.write(Dictionary['questionnaire'][p]["Speaker"]+"\n")
            for n in Dictionary['questionnaire'][p]["Remark"]:
                f.write(n+"\n\n")
    f.close()
    os.chdir(D2)
    h=h+1
n=0
os.chdir(D4)
lot=os.listdir(os.getcwd())
pi={}
fileno=0
df={}
tf={}
idf={}
lemma=WordNetLemmatizer()
docll=0

# del string
import string 
for fi in lot:
     file=io.open(fi,encoding="utf-8")
     fr=file.read()
     # print(fi)
     n=n+1
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
     for word in sofwords:
         # For each word, the list of docs containing words
         if (word in df):
            if str(fi) not in df[word]: 
               df[word].append(str(fi))
         else:
             df[word]=[]
             df[word].append(str(fi))
         # Counting frequency
         if (word in tf):
             if fi in tf[word]:
                 tf[word][fi]=tf[word][fi]+1
             else:
                 tf[word][fi]=1
         else:
             tf[word]={}
             tf[word][fi]=1
# calculating tf and idf
for w in tf:
    for docu in tf[w]:
        tf[w][docu]=log10(1+tf[w][docu])

doclp=1
# idf={}
for word in df:
    idf[word]=log10(n/len(df[word]))

# Inverted positional index 
iposi={}
for word in idf:
    iposi[(word,idf[word])]=tf[word]

os.chdir(mainfolder+"/Dataset")
f1=open('StaticQualityScore.pkl','rb')
static_score=pickle.load(f1)

chlil={}
chlig={}
for word,id in iposi:
   chlil[word]={z: v for z, v in sorted(iposi[(word,id)].items(), key=lambda item: item[1], reverse=True)}
   chlil[word]=dict(itertools.islice(chlil[word].items(),50))

   # Calculating the tfidf values 
   tfidf={}
   for t in iposi[(word,id)]:
       tfidf[t]=iposi[(word,id)][t]*id+static_score[int(t[:-4])]
   chlig[word]={z: v for z, v in sorted(tfidf.items(), key=lambda item: item[1], reverse=True)}
   chlig[word]=dict(itertools.islice(chlig[word].items(),50))
t_voc=len(iposi)
v={}
#the tf idf vectors
i=0

while count_sven < azp:
    for word,id in iposi:
        for t in iposi[(word,id)]:
            if t in v:
                v[t][i]=iposi[(word,id)][t]*id*doclp
            else:
                v[t]=[0]*t_voc*doclp
                v[t][i]=iposi[(word,id)][t]*id*doclp
        i=i+1
    count_sven += 1
fl=open('Leaders.pkl','rb')
leaders=pickle.load(fl)
os.chdir(mainfolder)
# fq=open('query.txt','r',encoding="utf-8")
fq=open('%s'%sys.argv[1],'r',encoding="utf-8")
loflines=fq.readlines()
fR=open("RESULTS2_19EC30040.txt","w+",encoding="utf-8")
for line in loflines:
    data=line.strip()
    # first we lowercase
    data=np.char.lower(data)
    # taking care of Stop words
    stop_words = stopwords.words('english')
    sofwords = word_tokenize(str(data))
    n_txt = ""
    rom1=0
    rom2=1
    for w in sofwords:
        if w not in stop_words and len(w) > 1:
            n_txt = n_txt + " " + w
    data=n_txt
    lofsymbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    # to remove puctuation
    for i in range(len(lofsymbols)):
        data = np.char.replace(data, lofsymbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    data = np.char.replace(data, "'", "")
    sofwords=word_tokenize(str(data))
    # words=[lemma.lemmatize(w) for w in words]
    i=0;
    t_num = 1
    for w in sofwords:
         # w=w.lower()
         sofwords[i]=lemma.lemmatize(w)
         # sofwords[i]=sofwords[i].lower()
         i=i+1
    q=[0]*t_voc
    i=0
    for word,id in iposi:
       if word in sofwords:
           q[i]=id
       i=i+1
    count_sven=1
    q_norrm=LA.norm(q)
    # initialising the scores
    t_doc = 0
    score_1={}
    score_2={}
    score_4={}
    score_3={}
    while rom1<rom2:
        for doc in v:
            v_norm=LA.norm(v[doc])+docll
            score_1[doc]=np.dot(v[doc],q)/(v_norm*q_norrm*doclp)
            # score_1[doc]=res
        for term in sofwords:
            if (term in chlil):
                for doc in chlil[term]:
                    v_norm=LA.norm(v[doc])+docll
                    score_2[doc]=np.dot(v[doc],q)/(v_norm*q_norrm*doclp)
                    # score_2[doc]
            if (term in chlig):
                for doc in chlig[term]:
                    v_norm=LA.norm(v[doc])+docll
                    score_3[doc]=np.dot(v[doc],q)/(v_norm*q_norrm*doclp)
        rom1=rom1+1
                # score_3[doc]
    # trying to find the leader from the leader list for this query
    lead=""
    max=0
    while count_sven <= azp:
        for docid in leaders:
            doc=str(docid)+".txt"
            v_norm=LA.norm(v[doc])+docll
            res=np.dot(v[doc],q)/(v_norm*q_norrm*doclp)
            if (res>=max) :
                max=res
                lead=doc
        count_sven += 1
    if (lead==""):
       lead="0.txt"
    # in order to assign a random file if no leader is found
    lead_norm=LA.norm(v[lead])
    follower=[]
    while t_doc < t_num:
        for doc1 in v:
            if doc1==lead:
                continue
            doc1_norm=LA.norm(v[doc1])+docll
            res=np.dot(v[doc1],v[lead])/(doc1_norm*lead_norm*doclp)
            flag=0
            for doc2 in leaders:
                doc=str(doc2)+".txt"
                if doc==lead:
                    continue
                doc_norm=LA.norm(v[doc])+docll
                ress1=docll
                ress1=np.dot(v[doc1],v[doc])/(doc1_norm*doc_norm*doclp)
                if (ress1+docll>res):
                    flag=1
                    break
            if (flag==0):
                follower.append(doc1)
        t_doc += 1
    
    follower.append(lead)
    # score_4={}
    count_bit = azp
    for doc in follower:
        v_norm=LA.norm(v[doc])+docll
        score_4[doc]=np.dot(v[doc],q)/(v_norm*q_norrm*doclp)
        # score_4[doc]
    while t_doc <= t_num:
        score_1={z: v for z, v in sorted(score_1.items(), key=lambda item: item[1], reverse=True)}
        score_2={z: v for z, v in sorted(score_2.items(), key=lambda item: item[1], reverse=True)}
        
        score_3={z: v for z, v in sorted(score_3.items(), key=lambda item: item[1], reverse=True)}
        
        score_4={z: v for z, v in sorted(score_4.items(), key=lambda item: item[1], reverse=True)}
        
        # score_4=score_4.items()
        # score_4=list(score_4)[:10]
        t_doc += 1

    # print(line.strip())
    # print(score_1)
    # print(score_2)
    # print(score_3)
    # print(score_4)
    # print()
    # fR=open("RESULTS2_19EC30040.txt","w+",encoding="utf-8")
    fR.write(line.strip()+"\n")
    # print("YES")
    # fR.write("\n")
    # flag=0
    writefunc(score_1,score_2,score_3,score_4,fR)
fR.close()