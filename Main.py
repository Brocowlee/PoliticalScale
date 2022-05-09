from re import search
import tweepy
import csv
import pandas as pd
import twitter_keys
import time

#Setup access to API
auth = tweepy.OAuthHandler(twitter_keys.twitter_keys_dico['API_key'], twitter_keys.twitter_keys_dico['API_secret'])
auth.set_access_token(twitter_keys.twitter_keys_dico['access_token_key'], twitter_keys.twitter_keys_dico['access_token_secret'])

api = tweepy.API(auth,wait_on_rate_limit=True)

#check du bon fonctionnement de mes codes d'authentification
try:
    api.verify_credentials()
    print("all good")
except:
    print("troubles...")



def get_follows(screenName):

    #version permettant l'obtention de la liste d'amis directement sans passer par les ids (nombre de requete trés limité)
    # follows_lst=tweepy.Cursor(api.get_friends,screen_name=screenName).items()
    # for friend in follows_lst:
    #     res.append(friend.screen_name)

    res=[]    
    follows_lst=tweepy.Cursor(api.get_friend_ids,screen_name=screenName).items()
    for friendID in follows_lst:
        res.append(api.get_user(user_id=friendID).screen_name)
    return res

def searchInCSV(lstFollows):
    cptPol=0
    EG=0
    G=0
    C=0
    D=0
    ED=0
    data=pd.read_csv("PolitiqueFR_Twitter.csv",delimiter=',')
    for follows in lstFollows:
        for i in range(len(data["screen_name"])):
            if data["screen_name"][i]==follows:
                cptPol+=1
                if data["OrientationPol"][i]=="EG":
                    EG+=1
                elif data["OrientationPol"][i]=="G":
                    G+=1
                elif data["OrientationPol"][i]=="C":
                    C+=1
                elif data["OrientationPol"][i]=="D":
                    D+=1
                elif data["OrientationPol"][i]=="ED":
                    ED+=1
    return cptPol,EG,G,C,D,ED

def displayScore(lstFollows):
    cptPol,EG,G,C,D,ED=searchInCSV(lstFollows)
    print("nombre de politiques suivie:"+str(cptPol)+"\n"+"nombre de comptes suivies:"+str(len(lstFollows))+"\n"+"EG:"+str(EG)+"\n"+"G:"+str(G)+"\n"+"C:"+str(C)+"\n"+"D:"+str(D)+"\n"+"ED:"+str(ED)+"\n")

def displayScoreSN(SN):
    follow_list=get_follows(SN)
    displayScore(follow_list)

#displayScoreSN("EmmanuelMacron")
#displayScoreSN("NPolony")
#displayScoreSN("fhollande")
displayScoreSN("ZemmourEric")
