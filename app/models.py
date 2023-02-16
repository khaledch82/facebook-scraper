from sqlalchemy import Column, Integer, String
from config.database import engine, Base


class Post(Base):
    """ Create scraper model."""
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(500))
    link = Column(String(500))
    nb_likes = Column(Integer)
    nb_comments = Column(Integer)


Base.metadata.create_all(engine)
