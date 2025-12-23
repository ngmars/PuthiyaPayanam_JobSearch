from .. import jobModels as models
from sqlalchemy.orm import Session
from ...utils import writeToDb

def checkDbForCompany(db: Session, company_name: str):
    company = db.query(models.Company).filter(models.Company.company_name == company_name).first()
    if(company is None):
        new_company = models.Company(
            company_name=company_name
        )    
        return writeToDb(new_company, db)       
    return company

def getCompanyById(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()



