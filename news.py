import newsapi
from newsapi.const import SOURCES_URL
from pandas.io import json
import requests
import pandas as pd
from newapi_config import newsapi_key
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key=newsapi_key)


#top_headlines = f"https://newsapi.org/v2/top-headlines?country=hk&apiKey={newsapi_key}"

everything = f"https://newsapi.org/v2/top-headlines?country=hk&category=business&from=2021-06-03&to=2021-06-20&apiKey={newsapi_key}"

#source = requests.get(top_headlines)

sourcetwo = requests.get(everything)

#jstring = source.json()

jstringtwo = sourcetwo.json()

#article = jstring['articles']

#df = pd.DataFrame(article)

#data = df[["publishedAt", "source", "title", "description"]]


#title = article['title']

#data = json.loads(jstring)


#data.to_csv('data2.csv', index=False)
# print(datatwo)
print(jstringtwo)
# print(source.json())
