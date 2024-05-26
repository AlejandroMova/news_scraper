from seleniumbase import SB
from textblob import TextBlob
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import csv

load_dotenv()

def get_database(): 

    CONNECTION_STRING = os.getenv('CONNECTION_STRING')
    client = MongoClient(CONNECTION_STRING)
    return client['articles-with-sentiment']

def analyze_sentiment(articles): 
    for article in articles: 
        blob = TextBlob(article['title'])
        article['sentiment'] = blob.sentiment.polarity 
    return articles

with SB(uc=True) as sb: 

    # scrape for articles
    sb.driver.uc_open('https://edition.cnn.com/politics')

    titles = sb.find_elements('.container__link ')

    articles = []

    # add to articles list as dictionary
    for title in titles: 
        articles.append({'title': title.text, 'url': title.get_attribute('href')})


    # add sentiment to articles
    articles_with_sentiment = analyze_sentiment(articles)

    # add id to dictionaries
    for index, article in enumerate(articles_with_sentiment): 

        article['_id'] = str(index)

    # initialize database
    dbname = get_database()
    collection_name = dbname["articles"]

   
    # insert into database
    # collection_name.insert_many(articles_with_sentiment)

    # insert into a csv file
    filename = 'articles.csv'

    fields = ['title', 'url', 'sentiment', '_id']
    rows = []

    # add info into rows

    for article in articles_with_sentiment: 
        rows.append([article['title'], article['url'], article['sentiment'], article['_id']])
    
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)
        