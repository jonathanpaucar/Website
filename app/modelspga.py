from sqlalchemy import Column, Float, String, Integer, Numeric
from .database import Base

class pga(Base):
    __tablename__ = "pga"
    player = Column(String, unique=True, index=True)
    numofrounds = Column(Integer)
    avgapproach = Column(Integer)
    totalapproach= Column(Integer)
    pergreensinreg= Column(Integer)
    greenshitinreg= Column(Integer)
    numholes= Column(Integer)
