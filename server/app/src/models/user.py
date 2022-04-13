from sqlalchemy import Column, Integer, String, Boolean, Float, event
from sqlalchemy.orm import relationship

from .. import db

class User(db.Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    amount = Column(Float, nullable=False)