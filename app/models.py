from sqlalchemy import Column, Float, String, Integer, Numeric
from .database import Base

class salary(Base):
    __tablename__ = "salary"
    id = Column(Integer, primary_key=True, index=True)
    player = Column(String, unique=True, index=True)
    fieldposition = Column(String)
    team = Column(String)
    salary= Column(Numeric)
