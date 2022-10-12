import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, BigInteger, Boolean, TIMESTAMP
from db.db_conf import Base

load_dotenv()

class Ping(Base):

    __tablename__ = 'ping'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(800), nullable=False)

    def __repr__(self):
        return '<Ping %r>' % self.id