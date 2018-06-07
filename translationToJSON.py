import nltk
import enchant
import pycountry
import sys
import json
import string
import re
from worldcupleadertweets import get_all_tweets,screen_names
from googletrans import Translator

dictionary = None
countryDict = None
translate = None

def remove_emojis(line):
    emoji_pattern = re.compile(u"([\U0001F600-\U0001F64F]|[\U0001F300-\U0001F5FF]|[\U0001F680-\U0001F6FF]|[\U0001F1E0-\U0001F1FF])+", flags=re.UNICODE)
                                # emoticons  # symbols & pictographs
                                 # transport & map symbols
                                 # flags (iOS),
    return emoji_pattern.sub(r'', line)  # no emoji

def splitElimination(line):
    words = line.split()
    newline = []
    for word in words:
        word = remove_emojis(word)
        if word != '' and word[0] == '#':
            newline.append(word[1:])
        elif word != '' and 'http' not in word and word[0] != '@':
            newline.append(word)

    return ' '.join(newline)

def translation(line):
    here = splitElimination(line)
    return (translate.translate(here)).text

def process_names(tokens):
    here = nltk.ne_chunk(nltk.pos_tag(tokens))
    sent = ''
    for x in here:
        if not hasattr(x, 'label') and not isinstance(x, nltk.Tree):
            sent = sent + " " + x[0]
    return sent

def checkForEnglish(line):
    global dictionary
    if dictionary == None:
        dictionary = enchant.Dict("en_US")
    removePunc = "".join((char for char in line if char not in string.punctuation))
    tokens = removePunc.split(" ")
    newline = []
    for word in tokens:
        if len(word) > 0 and dictionary.check(word.lower()) and not checkCountry(word):
            newline.append(word)

    return newline

def checkCountry(word):
    return word.lower() in countryDict

def process(chunk):
    global translate
    # print (process_names(checkForEnglish(translation(chunk))))
    try:
        return process_names(checkForEnglish(translation(chunk))) + " "
    except:
        try:
            translate = Translator()
            return process_names(checkForEnglish(translation(chunk))) + " "
        except:
            return ""

def translateTweetsJson(screen_name, include_retweets=False, saveTweets=False, saveTranslation=False, quant=4000):
    global translate
    global countryDict
    if translate == None:
        translate = Translator()

    if countryDict == None:
        countryDict = {}
        for country in pycountry.countries:
            countryDict[country.name.lower()] = 0

    tweetDict = get_all_tweets(screen_name, include_retweets, save=saveTweets, dict_output=True, quant=quant)
    content = (tweetDict[1]["content"]).split(" ")
    output = ""
    chunk = ""
    for word in content:
        if sys.getsizeof(chunk) > 1000:
            output += (re.sub(' +', ' ', process(chunk))).lower()
            chunk = ""

        if sys.getsizeof(word) < 1000:
            chunk += word + " "

    output += process(chunk)
    tweetDict[1]["content"] = output

    if saveTranslation:
        with open("JSONs/" + screen_name.lower()+'.json', "w") as f:
            data = json.dumps(tweetDict)
            f.write(data)

    return tweetDict


for s in screen_names:
    print s
    translateTweetsJson(s, False, False, True)
    print s,'done'

