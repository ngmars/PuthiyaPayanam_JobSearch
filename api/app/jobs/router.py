from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..auth.oauth import get_current_user
from . import jobModels as models
from . import jobSchemas as schemas

from .utils import companyDbQuery as utils
from ..utils import writeToDb

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/create", response_model=schemas.JobOut)
def create_job(
        job: schemas.JobCreate,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):

    company = utils.checkDbForCompany(
        db=db,
        company_name=job.company_name
    )

    print("Company ID:", company.id)

    new_job = models.Job(
        title=job.title,
        description=job.description,
        location=job.location,
        company_name=job.company_name,
        company_id=company.id,
        posted_by=current_user.id
    )
    new_job = writeToDb(new_job, db)
    return new_job


# Get all jobs
@router.get("/all", response_model=List[schemas.JobOut])
def get_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).all()
    return jobs
