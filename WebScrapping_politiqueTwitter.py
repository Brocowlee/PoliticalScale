from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

data=pd.read_csv("PolitiqueFR_Twitter.csv")
urls=["http://ymobactus.miaouw.net/labo-politiques.php?tendance=ExtremeDroite","https://ymobactus.miaouw.net/labo-politiques.php?tendance=Gauche","https://ymobactus.miaouw.net/labo-politiques.php?tendance=Centre","https://ymobactus.miaouw.net/labo-politiques.php?tendance=Droite","https://ymobactus.miaouw.net/labo-politiques.php?tendance=ExtremeGauche"]

def findText(text):
    YMA="YMA_Click_Profile('"
    res=""
    for index in range(len(text)):
        i=0
        while text[index+i]==YMA[i]:
            i+=1
            if i==len(YMA):
                t=index+len(YMA)
                secu=0
                while text[t]!="\'" or secu==50:
                    res+=text[t]
                    t+=1
                    secu+=1
                return res
    return -1

def initCSV():
    nbtour=0
    for url in urls:
        nbtour+=1
        result= requests.get(url)
        soup = BeautifulSoup(result.text, "html.parser")
        tag=soup.find_all("a")
        for e in tag:
            if findText(str(e)) != -1:
                data.at[len(data["screen_name"]),"screen_name"]=findText(str(e))
                if nbtour==1:
                    data.at[len(data["OrientationPol"])-1,"OrientationPol"]="ED"
                elif nbtour==2:
                    data.at[len(data["OrientationPol"])-1,"OrientationPol"]="G"
                elif nbtour==3:
                    data.at[len(data["OrientationPol"])-1,"OrientationPol"]="C"
                elif nbtour==4:
                    data.at[len(data["OrientationPol"])-1,"OrientationPol"]="D"
                elif nbtour==5:
                    data.at[len(data["OrientationPol"])-1,"OrientationPol"]="EG"
    data.to_csv('PolitiqueFR_Twitter.csv',sep=',')

initCSV()