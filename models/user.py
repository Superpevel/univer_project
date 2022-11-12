import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, BigInteger, Boolean, TIMESTAMP
from db.db_conf import Base

load_dotenv()

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(800), nullable=False)
    password = Column(String(800), nullable=False)
    email = Column(String(1000), nullable=True)
    token = Column(String(), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id