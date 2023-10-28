import datetime as dt
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from newsapi import NewsApiClient
from pydantic import BaseModel, HttpUrl, Field
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
@app.post('/top/{country}', response_class=HTMLResponse)
def get_country_top_news(request: Request, country: str):
    db_news = topnews.find_one({'country': country})
    if db_news is None:
        query = api.get_top_headlines(country=country, language=None)
        data = query['articles']
        articles = [
            {'title': item['title'],
             'url': item['url'],
             'img': item['urlToImage'] or 'https://picsum.photos/640/120'}
           for item in data
        ]
        document = {
            'country': country,
            'time': dt.datetime.now(),
            'articles': articles
        }
        topnews.insert_one(document)
    else:
        articles = db_news['articles']
    return templates.TemplateResponse('topnews.html', {'request': request, 'news': articles})

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'countries': countries})

@app.post('/', response_class=RedirectResponse)
def get_country(request: Request, country: str = Form()):
    country = country.title()
    redirect_url = request.url_for('get_country_top_news', country=countries[country])
    return RedirectResponse(redirect_url)

