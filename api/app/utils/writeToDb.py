from sqlalchemy.orm import Session

def writeToDb(data: dict, db: Session):
    db.add(data)
    db.commit()
    db.refresh(data)
    return data