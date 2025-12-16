from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from . import userModels as models
from ..auth.oauth import get_current_user
from ..utils import awsS3Connect
from . import userSchemas as schemas
from .utils import linksUtils

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/userDataLinks", response_model=List[schemas.userDetailsOut])
def get_user_data_links(
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
    print("Current User ID:", current_user.id)
    existing_links = db.query(models.UserDataLinks).filter(models.UserDataLinks.user_id == current_user.id).all()
    return existing_links


@router.post("/userDataLinks/create", response_model=schemas.userDetailsOut)
def create_user_data_link(
        link: schemas.userDetailsCreate, 
        current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)
    ):
    existing_links = db.query(models.UserDataLinks).filter(models.UserDataLinks.user_id == current_user.id).all()
    if(link.is_cv):
        raise HTTPException(status_code=400, detail="CV link cannot be created here")
    
    return linksUtils.write_links_to_db(
        db=db,
        current_user=current_user,
        link=link,
        existing_links=existing_links
    )

   
 

@router.post("/userDataLinks/uploadCv", response_model=schemas.userDetailsOut)
def upload_cv_to_s3(
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db),
        file: UploadFile = File(...)
    ):
    """
        This is the endpoint to upload CV to S3 and store the link in the database

        Args:
            current_user: models.User = Depends(get_current_user)
            db: Session = Depends(get_db)
            File: UploadFile = File(...)

        Returns:
            schemas.userDetailsOut: The userDetailsOut schema with the CV link details.

        Author: Nitish Gopinath
        Date: 12th December 2025
   """
    allowed_extensions = {"pdf", "txt"}
    ext = file.filename.split(".")[-1].lower()
    print("File extension:", ext)
    if ext not in allowed_extensions:
        raise HTTPException(400, f"Unsupported file type: {ext}")

    # --- Create S3 filename ---
    s3_filename = f"CVs/user_{current_user.id}_cv.{ext}"
    print("S3 Filename:", s3_filename)

    # --- Upload to S3 ---
    s3_url = awsS3Connect.upload_file_to_s3(
        file=file.file,
        filename=s3_filename
    )
    if not s3_url:
        raise HTTPException(500, "Failed to upload file to S3")
    
    # --- Store link in DB ---

    existing_cv_link = db.query(models.UserDataLinks).filter(
        models.UserDataLinks.user_id == current_user.id,
        models.UserDataLinks.is_cv == True
    ).all()
    
    print("Existing CV Link:", existing_cv_link)
    link = {
        "website_link": s3_url,
        "is_cv": True,
        "is_linkedIn": False,
        "is_github": False,
        "other_site": None
    }
    return linksUtils.write_links_to_db(
        db=db,
        current_user=current_user,
        link=link,
        existing_links=existing_cv_link
    )
