from sqlalchemy.orm import Session
from models import Post
from scraper import FacebookScraper


def create_scraper(session: Session, url: str):
    """Scrapes a facebook public page"""
    try:
        facebook_scraper = FacebookScraper(url)
        (post_links, texts, nb_likes, nb_comments) = facebook_scraper.scrape_post()
        for c in range(len(post_links)):
            post = Post(link=post_links[c], text=texts[c], nb_likes=nb_likes[c], nb_comments=nb_comments[c])
            session.add(post)
            session.commit()
            session.refresh(post)
        return "scraped posts saved in database"
    except Exception as e:
        print(e)
