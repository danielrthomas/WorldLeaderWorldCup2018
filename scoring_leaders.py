# from elastic_search
ES_HOST = {
    "host": "localhost",
    "port": 9200
}

from elasticsearch import Elasticsearch
from worldcupleadertweets import *
from translationToJSON import translateTweetsJson
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import json

# create ES client, create index
es = Elasticsearch (hosts=[ES_HOST])

def lookup_leader(screen_name):
    print("searching...")
    doc = translateTweetsJson(screen_name, quant=25)
    # print (doc[1]["content"])
    res = es.search (body={
        'query': {
            'match': {
                'content': doc[1]["content"] ,
            }
        }
    })
    print ("Max score: ", res["hits"]["max_score"])
    i = 0
    while (res["hits"]["hits"][i]):
        print (res["hits"]["hits"][i]["_score"])
        i = i + 1
    return res


def get_terms_weights(content):
    leaders_content = []
    tfidf_vectorizer = TfidfVectorizer (max_df=0.85, min_df=2, stop_words='english')
    tfidf = tfidf_vectorizer.fit_transform (leaders_content)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names ()


def make_tweet_json():
    content = []
    screen_names = ["gudlaugurthor", "m_royalfamily"]
    for name in screen_names:
        with open ("JSONs/" + name.lower () + '.json', "r") as f:
            for line in f:
                data = json.loads(line)
                content.append(data[1]["content"])
    print (content)
    return content


def compute_idf():
    #initialize an empty vectorizer
    tfidf_vect = TfidfVectorizer()
    # tfidf_vect = TfidfVectorizer (max_df=0.85, min_df=2, stop_words='english')
    list_of_strings = make_tweet_json()
    #compute idf values for each world leader (list_of_strings has length 32)
    tfidf = tfidf_vect.fit(list_of_strings)

    print (tfidf.get_feature_names())
  #save the fitted vectorizer to use later
    pickle.dump(tfidf, open("some_file_name", "wb"))

# tfidf_vect = pickle.load("some_file_name")

def score_user(user_tweets = translateTweetsJson("realdonalTrump", False, False, False, 25)[1]["content"]):

    word_scores = []
    tfidf_vect = pickle.load (open("some_file_name", "rb"))

    # for unique_word in set(user_tweets.split(" ")):
    for unique_word in user_tweets.split(" "):

        #is the word in idf dictionary?
        # print (tfidf_vect.get_feature_names())
        print (unique_word)
        if unique_word in tfidf_vect.get_feature_names():
          #word importance weight

          idf_index = tfidf_vect.get_feature_names().index(unique_word)
          idf_score = tfidf_vect.idf_[idf_index]
          word_score = user_tweets.count(unique_word) * idf_score
          word_scores.append((word_score,unique_word))

    return word_scores





# translateTweetsJson("realdonalTrump", False, False, False, 25)[1]["content"]







