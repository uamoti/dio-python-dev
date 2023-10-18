from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from newsapi import NewsApiClient
from pydantic import BaseModel
# import requests

class News(BaseModel):
    title: str

with open('newsapi.key') as f:
    API_KEY = f.readline().strip()

api = NewsApiClient(API_KEY)
app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get('/top/{country}', response_class=HTMLResponse)
def get_country_top_news(request: Request, country: str) -> list[News]:
    query = api.get_top_headlines(country=country, language=None)
    articles = query['articles']
    news = [News(title=article['title']) for article in articles]
    return templates.TemplateResponse('index.html', {'request': request, 'news': news})

