from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models, database
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    encode_data = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    encode_data.update({"exp": expire})

    token = jwt.encode(encode_data, settings.secret_key, algorithm=settings.algorithm)

    return token

def verify_access_token(token: str, credentials_excepetion):

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_excepetion
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_excepetion

    # token data just id for now
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    '''
    a dependency in our path operations that will
    take the token from the request, verify the token,
    and extract the id.
    '''
    credentials_excepetion = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail=f"Could not validate credentials",
                                           headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_excepetion)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user