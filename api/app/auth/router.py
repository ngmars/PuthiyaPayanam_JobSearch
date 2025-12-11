from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..user import userModels as models
from ..user import userSchemas as schemas
from .utils import hash_password, verify_password
from .oauth import create_access_token, get_current_user
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model = schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # check if a user exists
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = models.User(
        name = user.name,
        email = user.email,
        hashed_password = hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, details="Invalid credentails")

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token":token, "token_type":"bearer"}

@router.post("/userid")
def returnUserId(current_user: models.User = Depends(get_current_user)):
    return{
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }

@router.post("/logout")
def logout():
    # stateless JWT means logout is clientside
    return ({
        "message": "Logout successful (client should delete token)"
    })
