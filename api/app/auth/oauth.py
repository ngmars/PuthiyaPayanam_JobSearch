from datetime import datetime, timedelta
from jose import jwt
from ..config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from ..config import settings
from ..user import userModels as models
from ..database import get_db
from sqlalchemy.orm import Session

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "auth/login")

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid Credential",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms = [settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if(user_id is None):
            raise credentials_exception

    except JWTError:
        raise credentials_exception

        # Fetch user from DB
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user

