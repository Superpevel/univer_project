import logging.config
from typing import List
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Request, Response, Depends, Header
from fastapi.responses import JSONResponse
from logs.logs_config import LOGGING_CONFIG
import logging
from db.db_conf import get_db
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models.card import Card
from schemas.request_schemas.ping_schema import PingRequest
from models.ping import Ping
from sqlalchemy.orm import Session
from schemas.request_schemas.card_request import CardDelete, CardRequest, UserRegister, UserLogin, InvoiceRequest
from models.user import User
from models.invoice import Invoice
import jwt

load_dotenv()

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI()
origins = ["*"]

@app.middleware('http')
def catch_exceptions_middleware(request: Request, call_next):
    try:
        return call_next(request)
    except Exception as e:
        logger.exception(e)
        return Response('Internal server error', status_code=500)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def secure(token):
    print(token)
    decoded_token = jwt.decode(token, 'secret', algorithms='HS256', verify=False)
    print(decoded_token)
    # this is often used on the client side to encode the user's email address or other properties
    return decoded_token

@app.post('/ping')
def ping(request: PingRequest, db:Session=Depends(get_db)):
    logger.info(f"ping {request.text}")
    ping = Ping(text=request.text)
    db.add(ping)
    db.commit()
    return True


@app.post('/new_card')
def new_card(request: CardRequest, db:Session=Depends(get_db), authorization: str = Header(None)):
    try: 
        user_data = secure(authorization)
    except Exception as e:
        return 'Not valid token'

    request = dict(request)
    request['current_amount'] = request['amount']
    card = Card(**request, user_id=user_data['user_id'])
    db.add(card)
    db.commit()
    db.refresh(card)
    return card

@app.post('/new_invoice')
def new_card(request: InvoiceRequest, db:Session=Depends(get_db), authorization: str = Header(None)):
    try: 
        user_data = secure(authorization)
    except Exception as e:
        return 'Not valid token'

    card: Card = db.query(Card).filter(Card.id==request.card_id).first()
    if not card:
        return 'no such card'
    if (card.current_amount - request.amount) < 0:
        return 'amount is below 0'

    price = card.price*request.amount
    invoice = Invoice(amount=request.amount, card_id=request.card_id,price=price, user_id=user_data['user_id'])
    db.add(invoice)
    db.commit()
    card.current_amount = card.current_amount - request.amount
    db.add(card)
    db.commit()
    db.refresh(invoice)
    return invoice

@app.get('/get_cards')
def get_cards(db:Session=Depends(get_db)):
    cards = db.query(Card).all()
    return cards

@app.get('/get_cards_user')
def get_cards_user(db:Session=Depends(get_db), authorization: str = Header(None)):
    try: 
        user_data = secure(authorization)
    except Exception as e:
        return 'Not valid token'

    cards = db.query(Card).filter(Card.user_id==user_data['user_id']).all()
    return cards

@app.post('/get_invoice_user')
def get_cards(db:Session=Depends(get_db), authorization: str = Header(None)):
    try: 
        user_data = secure(authorization)
    except Exception as e:
        return 'Not valid token'

    invoice = db.query(Invoice.id, Invoice.card_id, Invoice.price, Invoice.amount,Invoice.user_id, Card.title).filter(Invoice.user_id==user_data['user_id']).join(Card).all()
    return invoice

@app.post('/get_info_user')
def get_info_user(authorization: str = Header(None)):
    try: 
        user_data = secure(authorization)
    except Exception as e:
        return 'Not valid token'

    return user_data['user_id']

@app.post('/register')
def register(request: UserRegister, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.login==request.login).first()
    if user:
        return {'error': 'user is already registred'}
    obj: User = db.query(User).order_by(User.id.desc()).first()
    id = obj.id + 1
    encoded_jwt = jwt.encode({"login": request.login, 'password': request.password, 'user_id': id}, "secret", algorithm="HS256")
    user = User(login=request.login, email=request.email, password=request.password, token=encoded_jwt)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post('/login')
def login(request: UserLogin, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.login==request.login,).first()
    if not user:
        return {'error': 'No such user'}
    else:
        return user

@app.post('/delete_card')
def delete_card(request: CardDelete, db:Session=Depends(get_db), authorization: str = Header(None)):
    try: 
        user_data = secure(authorization)
    except Exception as e:
        return 'Not valid token'

    card: Card = db.query(Card).filter(Card.id==request.id,Card.user_id==user_data['user_id']).first()
    if card:
        db.delete(card)
        db.commit()
        return {'message': f'кароточка {card.title} удалена'}
    else:
        return {'message': 'такой карточке нету'}
if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8007, reload=True, debug=True)
