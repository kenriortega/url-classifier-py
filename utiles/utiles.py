from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import os
from sklearn.linear_model import LogisticRegression

import math
from collections import Counter


def extract_protocol(url: str) -> str:
    url_result = ""
    try:
        if url.startswith("https://"):
            url_result = url[8:]
        elif url.startswith("http://"):
            url_result = url[7:]
    except Exception as e:
        print(e)

    return url_result


def entropy(s):
    p, lns = Counter(s), float(len(s))
    return -sum(count / lns * math.log(count / lns, 2) for count in p.values())


def getTokens(input):
    tokensBySlash = str(input.encode('utf-8')).split('/')  # get tokens after splitting by slash
    allTokens = []
    for i in tokensBySlash:
        tokens = str(i).split('-')  # get tokens after splitting by dash
        tokensByDot = []
        for j in range(0, len(tokens)):
            tempTokens = str(tokens[j]).split('.')  # get tokens after splitting by dot
            tokensByDot = tokensByDot + tempTokens
        allTokens = allTokens + tokens + tokensByDot
    allTokens = list(set(allTokens))  # remove redundant tokens
    if 'com' in allTokens:
        allTokens.remove(
            'com')  # removing .com since it occurs a lot of times and it should not be included in our features
    return allTokens


def TL():
    allurls = './data/2.csv'  # path to our all urls file
    allurlscsv = pd.read_csv(allurls, ',', error_bad_lines=False)  # reading file
    allurlsdata = pd.DataFrame(allurlscsv)  # converting to a dataframe

    allurlsdata = np.array(allurlsdata)  # converting it into an array
    random.shuffle(allurlsdata)  # shuffling

    y = [d[1] for d in allurlsdata]  # all labels
    corpus = [d[0] for d in allurlsdata]  # all urls corresponding to a label (either good or bad)
    vectorizer = TfidfVectorizer(tokenizer=getTokens)  # get a vector for each url but use our customized tokenizer
    X = vectorizer.fit_transform(corpus)  # get the X vector

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                        random_state=42)  # split into training and testing set 80/20 ratio

    lgs = LogisticRegression()  # using logistic regression
    lgs.fit(X_train, y_train)
    print(lgs.score(X_test, y_test))  # pring the score. It comes out to be 98%
    return vectorizer, lgs


vectorizer, lgs = TL()


def show_index(path):
    X_predict = []
    X_predict.append(str(path))
    X_predict = vectorizer.transform(X_predict)
    y_Predict = lgs.predict(X_predict)
    return '''
You asked for %s

AI output: %s 
Entropy: %s 
''' % (path, str(y_Predict), str(entropy(path)))


# vectorizer, lgs = TL()
# checking some random URLs. The results come out to be expected. The first two are okay and the last four are malicious/phishing/bad

# X_predict = ['wikipedia.com','google.com/search=faizanahad','pakistanifacebookforever.com/getpassword.php/','www.radsport-voggel.de/wp-admin/includes/log.exe','ahrenhei.without-transfer.ru/nethost.exe','www.itidea.it/centroesteticosothys/img/_notes/gum.exe']

# X_predict = vectorizer.transform(X_predict)

# y_Predict = lgs.predict(X_predict)

# print(y_Predict)	#printing predicted values

# ``` This Repo is based on https://github.com/faizann24/Using-machine-learning-to-detect-malicious-URLs ```
# http://fsecurify.com/using-machine-learning-detect-malicious-urls/