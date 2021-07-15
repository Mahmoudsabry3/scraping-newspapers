#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import newspaper
from newspaper import Article
import pymongo
import dns
from collections import defaultdict
import pandas as pd
import nltk
nltk.download('punkt')


def get_urls(paper):
    """
    input :url of newspaper 
    return :the urls of the articles 
    
    """
    paper = newspaper.build(paper)

    url_list = []
    for article in paper.articles:
        url_list.append(article.url)
    return url_list


the_guardian = "https://www.theguardian.com"
bbc = "https://www.bbc.com"

the_guardian_urls = get_urls(the_guardian)
bbc_urls = get_urls(bbc)


# connect to mongoDB 
mongo  = pymongo.MongoClient("mongodb+srv://mahmoud:12345678910@cluster0.mgdgq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mydb = mongo['newspaper']
mycol = mydb['News']

# scrape  the data with newspaper package

def scrape_papers(articles_urls):
    """
    input :the urls of the articles
    return : dictionary that contains 
    the information from the articles
        
    """
    d = defaultdict(list)

    for each_paper in articles_urls:
        for url in each_paper:
            try:
                url_i = Article(url, language='en')
                url_i.download()
                url_i.parse()
                url_i.nlp()

                d['title'].append(url_i.title)
                d['author'].append(url_i.authors)
                d['time'].append(url_i.publish_date)
                d['URL'].append(url)
                d['keywords'].append(url_i.keywords)
                d['summary'].append(url_i.summary)
                d['text'].append(url_i.text)
            except:
                pass
    return d

d = scrape_papers([the_guardian_urls,bbc_urls])
df = pd.DataFrame.from_dict(d)
df.time = df.time.astype(str)
# save the data into MongoDB Atlas        
mycol.insert_many(df.to_dict('records'))

