
import json
# import re
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.tokenize import TweetTokenizer
# import os
# import io
import sys
#file=open('query.txt','r')
file=open('%s'%sys.argv[1],'r')
f2=open('postinglist.json','r')
f=open("RESULTS1_19EC30040.txt","w+",encoding='utf-8')
A=json.load(f2)
lines=file.readlines()
flag=0;
for s in lines:
    if(flag==1):
        f.write("\n")
    if(flag==0):
        flag=1
    s=s.strip()
    #f2=open('postinglist.json','r')
    #A=json.load(f2)
    l=len(s)
    if(s.startswith("*")):
        s=s[1:]
        for w in A:
            if w.endswith(s):
                f.write(w+":")
                #f.write(A[w][1])
                for fd in A[w][1]:
                    for po in A[w][1][fd]:
                        f.write("<"+fd+",%d>,"%po)
                f.write(";")
        #f.write("\n")
        continue
    if(s.endswith("*")):
        s=s[0:l-1]
        for w in A:
            if w.startswith(s):
                f.write(w+":")
                #f.write(A[w][1])
                for fd in A[w][1]:
                    for po in A[w][1][fd]:
                        f.write("<"+fd+",%d>,"%po)
                f.write(";")
        #f.write("\n")
        continue
    start=""
    end=""
    flag=1
    for c in s:
        if(c=='*'):
            flag=0
            continue
        if(flag==1):
            start=start+c
        else:
            end=end+c
    start=start.strip()
    end=end.strip()
    #print(start)
    #print(end)
    for w in A:
        if w.endswith(end) and w.startswith(start):
            f.write(w+":")
            #f.write(A[w][1])
            for fd in A[w][1]:
                for po in A[w][1][fd]:
                    f.write("<"+fd+",%d>,"%po)
            f.write(";")
    #f.write("\n")
print("Done")