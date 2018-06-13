ES_HOST = {
    "host": "localhost",
    "port": 9200
}

#from elasticsearch import Elasticsearch
from worldcupleadertweets import *
from translationToJSON import translateTweetsJson
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import json
import time
f = open("/home/infolab/apps/WorldCup/app/scorelog", "w")

# create ES client, create index
#es = Elasticsearch (hosts=[ES_HOST])

# def lookup_leader(screen_name):
#     print("searching...")
#     doc = translateTweetsJson(screen_name, quant=25)
#     # print (doc[1]["content"])
#     res = es.search (body={
#         'query': {
#             'match': {
#                 'content': doc[1]["content"] ,
#             }
#         }
#     })
#     print ("Max score: ", res["hits"]["max_score"])
#     i = 0
#     while (res["hits"]["hits"][i]):
#         print (res["hits"]["hits"][i]["_score"])
#         i = i + 1
#     return res



def compute_idf():
    # tfidf_vect = TfidfVectorizer(stop_words="english")
    vects = {}
    for name in screen_names:
        tfidf_vect = TfidfVectorizer (stop_words="english")
        try:
            with open ("/home/infolab/apps/WorldCup/app/JSONs/" + name.lower (), "r") as f:
                for line in f:
                    data = json.loads(line)
        except:
            with open ("JSONs/" + name.lower (), "r") as f:
                for line in f:
                    data = json.loads(line)

        tfidf = tfidf_vect.fit([data[1]['content']])
        vects[name.lower()] = tfidf
    try:
        pickle.dump(vects, open('/home/infolab/apps/WorldCup/app/pickle/some_file_name', "wb"))
    except:
        pickle.dump (vects, open ('pickle/some_file_name', "wb"))


# def compute_idf():
    #initialize an empty vectorizer
    # tfidf_vect = TfidfVectorizer (max_df=0.85, min_df=2, stop_words='english')

    # list_of_strings = make_tweet_json()
    #compute idf values for each world leader (list_of_strings has length 32)

    # print (tfidf.get_feature_names())
  #save the fitted vectorizer to use later
    # pickle.dump(tfidf, open("some_file_name", "wb"))

# tfidf_vect = pickle.load("some_file_name")

def leader_user_score(user_name,user_tweets):
    similar_scores = {}
    vectorizer = TfidfVectorizer (stop_words='english')
    fnew1 = open("/home/infolab/apps/WorldCup/app/leaderlog.log", "w")
    fnew1.write("iterating over leaders\n")
    for name in screen_names:
        try:
            with open ("/home/infolab/apps/WorldCup/app/JSONs/" + name.lower (), "r") as f:
                for line in f:
                    data = json.loads(line)
        except:
            with open ("JSONs/" + name.lower (), "r") as f:
                for line in f:
                    data = json.loads(line)
        fnew1.write("fitting\n")
        tfidf = vectorizer.fit_transform([user_tweets, data[1]["content"]])
        fnew1.write("fitted\n")
        #cosine similarity
        similar_scores[name] = ((tfidf * tfidf.T).A)[0, 1]
        fnew1.write("scores\n")

    return similar_scores


def score_user(user_handle,user_tweets,vects):
    fnew2 = open("/home/infolab/apps/WorldCup/app/userlog.log", "w")
    similar_word_scores = {}
    words = list (set (user_tweets.split (" ")))
    fnew2.write("iterating over leaders?\n")
    for name in screen_names:
        try:
            word_scores = []
            tfidf_vect = vects[name.lower()]

            # print (user_tweets)
            # for unique_word in set(user_tweets.split(" ")):
            # print (words)
            # exit()

            for unique_word in words:

                #is the word in idf dictionary?
                if unique_word in tfidf_vect.get_feature_names():
                  #word importance weight

                  idf_index = tfidf_vect.get_feature_names().index(unique_word)
                  idf_score = tfidf_vect.idf_[idf_index]
                  word_score = user_tweets.count(unique_word) * idf_score
                  word_scores.append((word_score,unique_word))
            fnew2.write("sorting word_scores\n")
            if word_scores != []:
                word_scores.sort (key=lambda x: x[0], reverse=True)
            fnew2.write("word_cores: " + str(word_scores) + '\n')
            if len(word_scores) < 5:
                word_scores = [('',''),('',''),('',''),('',''),('','')]
            similar_word_scores[name] = word_scores[:5]
            fnew2.write("adding to dict\n")
        except:
            fnew2.write("exception\n")
            similar_word_scores[name] = [('',''),('',''),('',''),('',''),('','')]
    fnew2.write("returning\n")
    return similar_word_scores


# compute_idf()
# print(score_user("jc_varela")["jc_varela"])
# print(score_user("realdonaldtrump"))


def match_handle(user_handle,vects):
    fnew = open("/home/infolab/apps/WorldCup/app/logscore.log", "w")
    fnew.write("matching handle")
    user_tweets = translateTweetsJson(user_handle, False, False, False, 100)[1]["content"]
    fnew.write("user_tweets: " + user_tweets)

    match_val = leader_user_score(user_handle,user_tweets)
    fnew.write("match_val: " + str(match_val))

    top_words = score_user(user_handle,user_tweets,vects)
    fnew.write("top_words: " + str(top_words))

    final_result = []
    for i,name in enumerate(screen_names):
        result = [match_val[name],leader_country[name],name,top_words[name]]
        final_result.append(result)

    final_result.sort(key=lambda  x:x[0], reverse=True)

    for i,result in enumerate(final_result):
        final_result[i].insert(0,i+1)
    return final_result

# print (match_handle("jc_varela"))
