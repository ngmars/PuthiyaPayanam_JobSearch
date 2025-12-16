from sqlalchemy import Column, Boolean, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Company(Base):
    __tablename__ = 'Company'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )
    company = relationship("JobPosting", back_populates="Company", cascade="all, delete")

class JobPosting(Base):
    __tablename__ = 'JobPosting'
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("Company.id", ondelete="CASCADE"), nullable=False)
    job_expiry = Column(TIMESTAMP(timezone=True), nullable=True)
    company = relationship("Company", back_populates="company")
    job_details = relationship("jobDetails", back_populates="job_posting", cascade="all, delete")
    
class jobDetails(Base):
    __tablename__ = 'JobDetails'
    id = Column(Integer, primary_key=True, index=True)
    job_posting_id = Column(Integer, ForeignKey("JobPosting.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(String, nullable=True)
    location = Column(String(100), nullable=True)
    is_remote = Column(Boolean, default=False)
    posted_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False
    )
    job_url = Column(String(255), unique=True, nullable=False)
    applications_count = Column(Integer, default=0)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )
    job_posting = relationship("JobPosting", back_populates="company")

