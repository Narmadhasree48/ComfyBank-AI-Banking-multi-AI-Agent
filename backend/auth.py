
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from database.models import Customer


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
def login_user(db: Session, phone: str, password: str):
    customer = db.query(Customer).filter(
    Customer.phone == phone
).first()

    if not customer:
        return None

    password_correct = pwd_context.verify(
        password,
        customer.password_hash
    )

    if not password_correct:
        print("Password incorrect")
        return None
    print("Password successful verified")
    return customer
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(account_number: str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": account_number,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scheme_name="BearerAuth"
)


def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        account_number = payload.get("sub")

        if account_number is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return account_number

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )