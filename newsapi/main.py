from fastapi import FastAPI
from newsapi import NewsApiClient
from pydantic import BaseModel
# import requests

class News(BaseModel):
    title: str

with open('newsapi.key') as f:
    API_KEY = f.readline().strip()

api = NewsApiClient(API_KEY)
app = FastAPI()

@app.get('/top/{country}')
def get_country_top_news(country: str) -> list[News]:
    query = api.get_top_headlines(country=country, language=None)
    articles = query['articles']
    
    return [News(title=news['title']) for news in articles]


