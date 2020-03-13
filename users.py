# -*- coding: utf-8 -*-
#import uuid

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key = True)
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
    print("Привет! Давай запишем твои личные данные")
    first_name =input("Введите свое имя: ")
    last_name = input("Введите свою фамилию: ")
    gender = input("Введите свой пол: ")
    email = input("Введите свой адрес электронной почты: ")
    birthdate = input("Введите дату своего рождения: ")
    height = input("Введите свой рост: ")
    

    user = User(
            first_name = first_name,
            last_name = last_name,
            gender = gender,
            email = email,
            birthdate = birthdate,
            height = height
            )
    return user

def main():
    session = connect_db()
    user  = request_data()
    session.add(user)
    session.commit()
    print("Данные сохранены")

if __name__ == "__main__":
    main()
    
    
    
    
    