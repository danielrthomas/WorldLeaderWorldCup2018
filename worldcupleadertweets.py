import base64
import requests
import sys
import csv
import re
import tweepy
from tweepy import OAuthHandler
import io

consumer_key = "PVWE9FmBmQr9JLTFZhFhWmm1p"
consumer_secret = "UcpPuhZ5RkKXPqkO89M64wF6Ta9vXrXcSCSZZZoqKR2n68lv1V"

access_key = '985628740662243335-SnY0Er1Y4Zoc4K5DjdvFoeo3A5A7CsN'
access_secret = 'ABd9yfrc1x6sZlHNLxRMO0izjXBSf0cT0e7zIeCe0p0VM'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

screen_names = ['gudlaugurthor', 'm_royalfamily', 'govkorea', 'topolanskylucia', 'sigmargabriel', 'antoniocostapm', 'margotwallstrom', 'kingsalman', 'kolindagk', 'theresa_may',
                'alain_berset', 'abeshinzo', 'macky_sall', 'putinrf_eng', 'larsloekke', 'avucic', 'alsisiofficial', 'bejiceofficial', 'mbuhari', 'rouhani_ir', 'epn', 'charlesmichel',
                'ppkamigo', 'emmanuelmacron', 'andrzejduda', 'mauriciomacri', 'turnbullmalcolm', 'micheltemer', 'jc_varela', 'juanmansantos', 'luisguillermosr', 'marianorajoy']

countries = ['Iceland','Morocco','South Korea','Uruguay','Germany','Portugal','Sweden','Saudi Arabia','Croatia','England','Switzerland','Japan','Senegal','Russia','Denmark','Serbia',
             'Egypt','Tunisia','Nigeria','Iran','Mexico','Belgium','Peru','France','Poland','Argentina','Australia','Brazil','Panama','Columbia','Costa Rica','Spain']

leader_country = {'mauriciomacri': 'Argentina', 'emmanuelmacron': 'France', 'juanmansantos': 'Columbia', 'mbuhari': 'Nigeria', 'putinrf_eng': 'Russia', 'alain_berset': 'Switzerland',
                  'larsloekke': 'Denmark', 'ppkamigo': 'Peru', 'micheltemer': 'Brazil', 'macky_sall': 'Senegal', 'margotwallstrom': 'Sweden', 'm_royalfamily': 'Morocco',
                  'topolanskylucia': 'Uruguay', 'govkorea': 'South Korea', 'rouhani_ir': 'Iran', 'abeshinzo': 'Japan', 'kingsalman': 'Saudi Arabia', 'sigmargabriel': 'Germany',
                  'luisguillermosr': 'Costa Rica', 'jc_varela': 'Panama', 'charlesmichel': 'Belgium', 'kolindagk': 'Croatia', 'marianorajoy': 'Spain', 'alsisiofficial': 'Egypt',
                  'epn': 'Mexico', 'bejiceofficial': 'Tunisia', 'theresa_may': 'England', 'andrzejduda': 'Poland', 'turnbullmalcolm': 'Australia', 'gudlaugurthor': 'Iceland',
                  'antoniocostapm': 'Portugal', 'avucic': 'Serbia'}


def get_all_tweets(screen_name,include_retweets=False,save=True,dict_output=False,quant=4000):
#Twitter only allows access to a users most recent 3240 tweets with this method

#authorize twitter, initialize tweepy

#initialize a list to hold all the tweepy Tweets
        alltweets = []	

#make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,tweet_mode='extended',include_rts=include_retweets)

#save most recent tweets
        alltweets.extend(new_tweets)

#save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

#keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0 and len(alltweets) < 4000:

#all subsiquent requests use the max_id param to prevent duplicates
                new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest,tweet_mode='extended',include_rts=include_retweets)

#save most recent tweets
                alltweets.extend(new_tweets)

#update the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1

#get the tweet text into an array	
        outtweets = [tweet.full_text for tweet in alltweets]

        try:
                outtweets = outtweets[:quant]
        except:
                pass

#save to a text file if the user has elected to save the output

        try:
                tweets = outtweets[0]
                for tweet in outtweets[1:]:
                        tweets += ' ' + tweet
        except:
                tweets = ''

        if dict_output:
                info_dict = {
                        "index" : {
                        '_index' : screen_name,
                        '_type' : "leaders",
                        '_id' : screen_name
                        }
                        }
                tweet_dict = {
                        "content" : tweets
                        }
                toreturn = []
                toreturn.append(info_dict)
                toreturn.append(tweet_dict)

                return toreturn
        
        elif save:

                title = screen_name
                
                if not include_retweets:
                        title += "-RT"

                with io.open(title+'.txt','w',encoding="utf-8") as f:

                        for tweet in outtweets:
                                f.write(tweet+u' ')

                result = [screen_name, len(outtweets)]

                return result

#return the result as a string instead
        else:
                try:
                        toreturn = outtweets[0]
                        for tweet in outtweets[1:]:
                                toreturn += u' '+ tweet
                except:
                        toreturn = u''
                return toreturn

##if __name__ == '__main__':
##        with open('results-RT.csv','wb') as csvfile:
##                writer = csv.writer(csvfile)
##                for name in screen_names:
##                        result = get_all_tweets(name)
##                        print result
##                        writer.writerow(result)
##
##        
##        with open('results.csv','wb') as csvfile:
##                writer = csv.writer(csvfile)
##                for name in screen_names:
##                        result = get_all_tweets(name,True)
##                        print result
##                        writer.writerow(result)
