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

screen_names = ['gudlaugurthor','M_RoyalFamily','govkorea','TopolanskyLucia','sigmargabriel','antoniocostapm','margotwallstrom','KingSalman','KolindaGK','theresa_may',
                'alain_berset','AbeShinzo','Macky_Sall','PutinRF_Eng','larsloekke','avucic','alsisiOfficial','bejiCEOfficial','Mbuhari','Rouhani_ir','EPN','CharlesMichel',
                'ppkamigo','EmmanuelMacron','AndrzejDuda','mauriciomacri','TurnbullMalcolm','MichelTemer','JC_Varela','JuanManSantos','luisguillermosr','marianorajoy']

def get_all_tweets(screen_name):
#Twitter only allows access to a users most recent 3240 tweets with this method

#authorize twitter, initialize tweepy

#initialize a list to hold all the tweepy Tweets
        alltweets = []	

#make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,tweet_mode='extended')

#save most recent tweets
        alltweets.extend(new_tweets)

#save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

#keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
##                print "getting tweets before %s" % (oldest)

#all subsiquent requests use the max_id param to prevent duplicates
                new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest,tweet_mode='extended')

#save most recent tweets
                alltweets.extend(new_tweets)

#update the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1

##                print "...%s tweets downloaded so far" % (len(alltweets))

#transform the tweepy tweets into a 2D array that will populate the csv	
        outtweets = [tweet.full_text for tweet in alltweets]#.encode("utf-8")

        with io.open(screen_name+'.txt','w',encoding="utf-8") as f:

                for tweet in outtweets:
                        f.write(tweet+u' ')

        result = [screen_name, len(outtweets)]

        return result

#write the csv	
##	with open('%s_tweets.csv' % screen_name, 'wb') as f:
##		writer = csv.writer(f)
##		writer.writerow(["id","created_at","text"])
##		writer.writerows(outtweets)

        pass

if __name__ == '__main__':
#pass in the username of the account you want to download
        with open('results.csv','wb') as csvfile:
                writer = csv.writer(csvfile)
                for name in screen_names:
                        result = get_all_tweets(name)
                        print result
                        writer.writerow(result)

##client_key = 'PVWE9FmBmQr9JLTFZhFhWmm1p'
##client_secret = 'UcpPuhZ5RkKXPqkO89M64wF6Ta9vXrXcSCSZZZoqKR2n68lv1V'

def main():
    for key in locations:
        location = locations[key]
        path = location.Name.replace(' ','_')+'.csv'
        print '\n\n',location.Name,'\n'
        
        tweet_data = query(location)

        print '\n','Results: ',len(tweet_data)
        
        old_tweets = {}
        try:
            reader = csv.reader(open(path,'r'))
            for row in reader:
                old_tweets[row[0]] = row
        except Exception as e:
            print str(e)

        added_count = 0
        for tweet in tweet_data:
            if tweet['id_str'] not in old_tweets:
                old_tweets[tweet['id_str']] = [tweet['id_str'],tweet['text'].encode('utf-8')]
                added_count += 1
            
        writer = csv.writer(open(path,'w'))
        for key in old_tweets:
            try:
                writer.writerow(old_tweets[key])
            except Exception as e:
                print old_tweets[key][1], str(e)

        print "\nAdded "+str(added_count)+" to "+location.Name

        choice = ''
        count = -1

##        while choice != 'y' and choice != 'n':
##            choice = raw_input('\nDo you want to print the tweets for '+location.Name+'? (y/n)\n')
##
##        if choice == 'y':
##            while count < 0:
##                count_a = raw_input("\nHow many?\n")
##                try:
##                    count = int(count_a)
##                except Exception as e:
##                    print str(e)
##
##            for i in range(0,count):
##                print '\n', tweet_data[i]['text'], ' | ', tweet_data[i]['place']

def query_helper(name="marianorajoy",max_id=None):
    key_secret = '{}:{}'.format(client_key, client_secret).encode('utf-8')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('utf-8')

    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

    access_token = auth_resp.json()['access_token']

    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)    
    }
    search_params = {
    'screen_name': name,
    'count': 100
    }
    if max_id != None:
        search_params['max_id'] = max_id

    search_url = '{}1.1/statuses/user_timeline.json'.format(base_url)

    search_resp = requests.get(search_url, headers=search_headers, params=search_params)

    print 'Status Code: ',search_resp.status_code

    tweet_data = search_resp.json()

    return tweet_data,search_resp.status_code

def query(name="marianorajoy"):
    doc = ''
    tweet_data = query_helper(name)
    max_id = None
    call_count = 1
    while max_id != sys.maxint:
        max_id = sys.maxint
        add = False
        toadd = ' '
        for tweet in tweet_data[0]:
            toadd += tweet['text']
            add = True
            if max_id > tweet['id']:
                max_id = tweet['id']
        print toadd
        toadd = ' '.join(toadd.splitlines())
        print toadd
        if add:
            doc += toadd
            max_id -= 1
        tweet_data = query_helper(name,max_id)
        call_count += 1
    print "\nCalls made: ",call_count
    return doc
