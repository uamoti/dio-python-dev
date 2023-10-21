from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from newsapi import NewsApiClient
from pydantic import BaseModel
from resources import countries
# import requests

class News(BaseModel):
    title: str

with open('newsapi.key') as f:
    API_KEY = f.readline().strip()

api = NewsApiClient(API_KEY)
app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.post('/top/{country}', response_class=HTMLResponse)
def get_country_top_news(request: Request, country: str):
    query = api.get_top_headlines(country=country, language=None)
    articles = query['articles']
    news = [News(title=article['title']) for article in articles]
    return templates.TemplateResponse('topnews.html', {'request': request, 'news': news})

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'countries': countries})

@app.post('/', response_class=RedirectResponse)
def get_country(request: Request, country: str = Form()):
    country = country.capitalize()
    redirect_url = request.url_for('get_country_top_news', country=countries[country])
    return RedirectResponse(redirect_url)

