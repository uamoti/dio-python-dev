import datetime as dt
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from newsapi import NewsApiClient
from pydantic import BaseModel, HttpUrl, Field
from pydantic_core.core_schema import list_schema
from resources import countries
from pymongo import MongoClient

class News(BaseModel):
    title: str
    url: HttpUrl
    img: HttpUrl

with open('newsapi.key') as f:
    API_KEY = f.readline().strip()

with open('mongo.uri') as f:
    MONGO_URI = f.readline().strip()

connection = MongoClient(MONGO_URI)
db = connection.newsapi
topnews = db.topnews
api = NewsApiClient(API_KEY)
app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

# If the collection is empty or the posts are old, then I query the API.
# Otherwise, retrieve the documents and display.

def get_country_top_news(country: str) -> list:
    db_news = topnews.find_one({'country': country})
    try:
        old_news = db_news['time'] + dt.timedelta(hours=12) < dt.datetime.now()
        _id = db_news['_id']
    except TypeError:
        old_news = True
        _id = None
    if old_news:
        query = api.get_top_headlines(country=country, language=None)
        data = query['articles']
        articles = [
            {'title': item['title'],
             'url': item['url'],
             'img': item['urlToImage'] or 'https://picsum.photos/1000/120'}
           for item in data
        ]
        document = {
            'country': country,
            'time': dt.datetime.now(),
            'articles': articles
        }
        if _id:
            topnews.delete_one({'_id': _id})
        topnews.insert_one(document)
    else:
        articles = db_news['articles']
    return articles

@app.get('/top/{country}', response_class=HTMLResponse)
@app.post('/top/{country}', response_class=HTMLResponse)
def country_topnews(request: Request, country: str):
    articles = get_country_top_news(country)
    return templates.TemplateResponse('topnews.html', {'request': request, 'news': articles})

@app.get('/', response_class=HTMLResponse)
# @app.post('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'countries': countries})

@app.post('/', response_class=RedirectResponse)
def get_country(request: Request, country: str = Form()):
    try:
        country = countries[country.title()]
        redirect_url = request.url_for('country_topnews', country=country)
    except KeyError:
        return RedirectResponse('/', status_code=302)
    return RedirectResponse(redirect_url)

