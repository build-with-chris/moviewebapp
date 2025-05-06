from flask import session
from flask_sqlalchemy.session import Session
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///data/users.sqlite', connect_args={'timeout': 10})
Session= sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String)

    def __repr__(self):
        return f"User(id = {self.user_id}, name = {self.user_name})"

class Movies(Base):
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    movie_name = Column(String)
    movie_director = Column(String)
    movie_year = Column(Integer)
    movie_rating = Column(Float)
