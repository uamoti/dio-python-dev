# NewsAPI Top News

The original project from the Python developer programme from [DIO](https://dio.me/en) was to query the Twitter/X trends API. This API is no longer free, so I switched to [NewsAPI](https://newsapi.org).

The goal is to get top news from a country and display to the user.
The country list is limited by the API.

The project uses FastAPI, Jinja2 and MongoDB.
I store the news of a country for 12 h in the DB; after that the news API is queried again.
