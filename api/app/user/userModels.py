from sqlalchemy import Column, Boolean, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(120), unique=True, index=True)
    hashed_password = Column(String(128))
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

    links = relationship("UserDataLinks", back_populates="user", cascade="all, delete")

class UserDataLinks(Base):
    __tablename__ = "user_data_links"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    website_link = Column(String(255), nullable =False)
    is_cv = Column(Boolean, default=False)
    is_linkedIn = Column(Boolean, default=False)
    is_github = Column(Boolean, default=False)
    other_site = Column(String(255), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

    user = relationship("User", back_populates="links")
