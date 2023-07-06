import json
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from models import Base, Film, Genre


engine = create_engine("sqlite:///my_db.db", echo=False)
session = Session(engine, autoflush=True)

def migrate():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    genres = [ Genre(**x) for x in json.load(open("data/films.json")).get("genres")]
    films = [ Film(**x, genre=genres[x.get('genre_id')]) for x in json.load(open("data/films.json")).get("films")]

    session.add_all(genres)
    session.add_all(films)
    session.commit()