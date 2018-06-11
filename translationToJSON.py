import nltk
##import enchant
##import pycountry
import sys
import json
import string
import re
from worldcupleadertweets import get_all_tweets,screen_names
from googletrans import Translator

dictionary = None
countryDict = None
translate = None

countries = [u'aruba', u'afghanistan', u'angola', u'anguilla', u'\xe5land islands', u'albania', u'andorra', u'united arab emirates', u'argentina', u'armenia', u'american samoa', u'antarctica', u'french southern territories', u'antigua and barbuda', u'australia', u'austria', u'azerbaijan', u'burundi', u'belgium', u'benin', u'bonaire, sint eustatius and saba', u'burkina faso', u'bangladesh', u'bulgaria', u'bahrain', u'bahamas', u'bosnia and herzegovina', u'saint barth\xe9lemy', u'belarus', u'belize', u'bermuda', u'bolivia, plurinational state of', u'brazil', u'barbados', u'brunei darussalam', u'bhutan', u'bouvet island', u'botswana', u'central african republic', u'canada', u'cocos (keeling) islands', u'switzerland', u'chile', u'china', u"c\xf4te d'ivoire", u'cameroon', u'congo, the democratic republic of the', u'congo', u'cook islands', u'colombia', u'comoros', u'cabo verde', u'costa rica', u'cuba', u'cura\xe7ao', u'christmas island', u'cayman islands', u'cyprus', u'czechia', u'germany', u'djibouti', u'dominica', u'denmark', u'dominican republic', u'algeria', u'ecuador', u'egypt', u'eritrea', u'western sahara', u'spain', u'estonia', u'ethiopia', u'finland', u'fiji', u'falkland islands (malvinas)', u'france', u'faroe islands', u'micronesia, federated states of', u'gabon', u'united kingdom', u'georgia', u'guernsey', u'ghana', u'gibraltar', u'guinea', u'guadeloupe', u'gambia', u'guinea-bissau', u'equatorial guinea', u'greece', u'grenada', u'greenland', u'guatemala', u'french guiana', u'guam', u'guyana', u'hong kong', u'heard island and mcdonald islands', u'honduras', u'croatia', u'haiti', u'hungary', u'indonesia', u'isle of man', u'india', u'british indian ocean territory', u'ireland', u'iran, islamic republic of', u'iraq', u'iceland', u'israel', u'italy', u'jamaica', u'jersey', u'jordan', u'japan', u'kazakhstan', u'kenya', u'kyrgyzstan', u'cambodia', u'kiribati', u'saint kitts and nevis', u'korea, republic of', u'kuwait', u"lao people's democratic republic", u'lebanon', u'liberia', u'libya', u'saint lucia', u'liechtenstein', u'sri lanka', u'lesotho', u'lithuania', u'luxembourg', u'latvia', u'macao', u'saint martin (french part)', u'morocco', u'monaco', u'moldova, republic of', u'madagascar', u'maldives', u'mexico', u'marshall islands', u'macedonia, republic of', u'mali', u'malta', u'myanmar', u'montenegro', u'mongolia', u'northern mariana islands', u'mozambique', u'mauritania', u'montserrat', u'martinique', u'mauritius', u'malawi', u'malaysia', u'mayotte', u'namibia', u'new caledonia', u'niger', u'norfolk island', u'nigeria', u'nicaragua', u'niue', u'netherlands', u'norway', u'nepal', u'nauru', u'new zealand', u'oman', u'pakistan', u'panama', u'pitcairn', u'peru', u'philippines', u'palau', u'papua new guinea', u'poland', u'puerto rico', u"korea, democratic people's republic of", u'portugal', u'paraguay', u'palestine, state of', u'french polynesia', u'qatar', u'r\xe9union', u'romania', u'russian federation', u'rwanda', u'saudi arabia', u'sudan', u'senegal', u'singapore', u'south georgia and the south sandwich islands', u'saint helena, ascension and tristan da cunha', u'svalbard and jan mayen', u'solomon islands', u'sierra leone', u'el salvador', u'san marino', u'somalia', u'saint pierre and miquelon', u'serbia', u'south sudan', u'sao tome and principe', u'suriname', u'slovakia', u'slovenia', u'sweden', u'swaziland', u'sint maarten (dutch part)', u'seychelles', u'syrian arab republic', u'turks and caicos islands', u'chad', u'togo', u'thailand', u'tajikistan', u'tokelau', u'turkmenistan', u'timor-leste', u'tonga', u'trinidad and tobago', u'tunisia', u'turkey', u'tuvalu', u'taiwan, province of china', u'tanzania, united republic of', u'uganda', u'ukraine', u'united states minor outlying islands', u'uruguay', u'united states', u'uzbekistan', u'holy see (vatican city state)', u'saint vincent and the grenadines', u'venezuela, bolivarian republic of', u'virgin islands, british', u'virgin islands, u.s.', u'viet nam', u'vanuatu', u'wallis and futuna', u'samoa', u'yemen', u'south africa', u'zambia', u'zimbabwe']

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

def checkForEnglish(line,dic):
    global dictionary
    dictionary = dic
##    if dictionary == None:
##        dictionary = enchant.Dict("en_US")
    removePunc = "".join((char for char in line if char not in string.punctuation))
    tokens = removePunc.split(" ")
    newline = []
    for word in tokens:
        if len(word) > 0 and dictionary.check(word.lower()) and not checkCountry(word):
            newline.append(word)

    return newline

def checkCountry(word):
    return word.lower() in countryDict

def process(chunk,dic):
    global translate
    # print (process_names(checkForEnglish(translation(chunk))))
    try:
        return process_names(checkForEnglish(translation(chunk)),dic) + " "
    except:
        try:
            translate = Translator()
            return process_names(checkForEnglish(translation(chunk)),dic) + " "
        except:
            return ""

def translateTweetsJson(screen_name, include_retweets=False, saveTweets=False, saveTranslation=False, quant=4000,dic=None):
    global translate
    global countryDict
    if translate == None:
        translate = Translator()

    if countryDict == None:
        countryDict = {}
##        for country in pycountry.countries:
        for country in countries:
            countryDict[country] = 0

    tweetDict = get_all_tweets(screen_name, include_retweets, save=saveTweets, dict_output=True, quant=quant)
    content = (tweetDict[1]["content"]).split(" ")
    output = ""
    chunk = ""
    for word in content:
        if sys.getsizeof(chunk) > 1000:
            output += (re.sub(' +', ' ', process(chunk,dic))).lower()
            chunk = ""

        if sys.getsizeof(word) < 1000:
            chunk += word + " "

    output += process(chunk,dic)
    tweetDict[1]["content"] = output

    if saveTranslation:
        with open("JSONs/" + screen_name.lower()+'.json', "w") as f:
            data = json.dumps(tweetDict)
            f.write(data)

    return tweetDict


# for s in screen_names:
#     print(s)
#     translateTweetsJson(s, False, False, True)
#     print(s,'done')
# print("sigmargabriel")
# translateTweetsJson("sigmargabriel", False, False, True)
# print('done')
