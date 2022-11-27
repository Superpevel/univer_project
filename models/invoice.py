import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, BigInteger, Boolean, TIMESTAMP,Float
from db.db_conf import Base


class Invoice(Base):

    __tablename__ = 'invoice'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    card_id = Column(Integer, ForeignKey("cards.id"))

    def __repr__(self):
        return '<Invoice %r>' % self.id