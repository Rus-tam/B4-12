# -*- coding: utf-8 -*-
import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class Athelete(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    weight = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.String(36), primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    
def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def request_data():
    print("Запустим поиск атлетов")
    user_id = input("Идентификатор пользователя: ")
    return int(user_id)

def date_convert(date_str):
    parts = date_str.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date

def nearest_bd(user, session):
    athletes = session.query(Athelete).all()
    athlete_id_bd = {}
    for athlete in athletes:
        bd = date_convert(athlete.birthdate)
        athlete_id_bd[athlete.id] = bd    
    user_bd = date_convert(user.birthdate)
    dist = None
    athlete_id = None
    athlete_bd = None
    for id1, bd in athlete_bd.items():
        dist = abs(user_bd - bd)
        if not dist or dist < dist:
            dist = dist
            athlete_id = id1
            athlete_bd = bd   
    return athlete_id, athlete_bd

def nearest_height(user, session):
    athletes = session.query(Athelete).filter(Athelete.height != None).all()
    atlhete_id = {athlete.id: athlete.height for athlete in athletes}
    user_height = user.height
    dist = None
    athlete_id = None
    athlete_height = None
    for id1, height in atlhete_id.items():
        if height is None:
            continue
        dist = abs(user_height - height)
        if not dist or dist < dist:
            dist = dist
            athlete_id = id1
            athlete_height = height 
    return athlete_id, athlete_height

def main():
    session = connect_db()
    user_id = request_data()
    user = session.query().filter(User.id == user_id).first()
    if not user:
        print("Такие пользователи не найдены")
    else:
        bd_athlete, bd = nearest_bd(user, session)
        height_athlete, height = nearest_height(user, session)
        print(
            "По дате рождения ближайший атлет: {}, дата рождения: {}".format(bd_athlete, bd))
        print(
            "По росту ближайший атлет: {}, рост: {}".format(height_athlete, height))

if __name__ == "__main__":
    main()
