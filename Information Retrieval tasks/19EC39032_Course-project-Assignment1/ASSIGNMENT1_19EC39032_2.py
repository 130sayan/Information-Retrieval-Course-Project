

from bs4 import BeautifulSoup
import re
# import pandas as pd
from datetime import datetime
from dateutil.parser import parse
import json
import os
import io
h=0
mainfolder=os.getcwd()
D2=mainfolder+"/ECT"
D3=mainfolder+"/ECTNestedDict"
if(os.path.isdir(D3)==False):
    os.mkdir(D3)
D4=mainfolder+"/ECTText"
if(os.path.isdir(D4)==False):
    os.mkdir(D4)
os.chdir(D2)
lof=os.listdir(os.getcwd())
lof=sorted(lof)
for fi in lof:
    file=io.open(fi,encoding="utf-8")
    print(fi)
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
    Questionnaire={}
    i=0
    k=j
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
            j=0;
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
    os.chdir(D3)
    dic1=open("Dic%d.json"%h,"w")
    json.dump(Dictionary,dic1)
    dic1.close()
    # D4=mainfolder+"/ECTText"
    os.chdir(D4)
    f=open("%d.txt"%h,"w+",encoding='utf-8')
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