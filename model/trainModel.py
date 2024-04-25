#文本情感分类

import pandas as pd
import numpy as np
import csv
from snownlp import SnowNLP
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def getSentiment_data():
    sentiment_data = []
    with open('./target.csv','r',encoding='utf8') as readerFile:
        reader = csv.reader(readerFile)
        for data in reader:
            sentiment_data.append(data)
    return sentiment_data

def model_train():
    sentiment_data = getSentiment_data()
    df = pd.DataFrame(sentiment_data,columns=['text','sentiment'])

    train_data,test_data = train_test_split(df,test_size=0.2,random_state=42)

    vectorize = TfidfVectorizer()
    X_train = vectorize.fit_transform(train_data['text'])
    y_train = train_data['sentiment']
    X_test = vectorize.transform(test_data['text'])
    y_test = test_data['sentiment']

    classifier = MultinomialNB()
    classifier.fit(X_train,y_train)

    y_pred = classifier.predict(X_test)

    # 计算进驻度
    accuracy = accuracy_score(y_test,y_pred)



if __name__ == "__main__":
    model_train()
