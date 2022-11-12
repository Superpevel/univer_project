from email.policy import default
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, BigInteger, Boolean, TIMESTAMP,Float
from db.db_conf import Base
import os
from dotenv import load_dotenv

load_dotenv()

class Card(Base):

    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True, index=True)
    main_photo = Column(String, default=os.environ.get('NO_IMAGE_PATH'))
    title = Column(String(800), nullable=False)
    comment = Column(String(), nullable=True)
    price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    def __repr__(self):
        return '<Card %r>' % self.id