from fastapi import APIRouter
from config.database import SessionLocal
from create_scraper import create_scraper
from models import Post
app = APIRouter()
session = SessionLocal()

# API to get scraping data from database

@app.get("/scrape/page")
async def get_scrapes():
    """ Get scraping data from database."""
    params = locals().copy()
    query = session.query(Post)
    for attr in [x for x in params if params[x] is not None]:
        query = query.filter(getattr(Post, attr).like(params[attr]))
    session.commit()
    return query.all()

# API to scrape a public facebook page and save results in a database

@app.post('/scrape/{page_name}')
async def scrape(page_name: str):
    """ scrape a facebook public page and save results in a database ."""
    try:
        return create_scraper(session, "https://m.facebook.com/"+page_name)
    except Exception as e:
        print(e)

@app.get('/')
def root_api():
    return {"message": "Welcome to facebook scraper"}
