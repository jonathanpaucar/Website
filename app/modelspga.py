from sqlalchemy import Column, Float, String, Integer, Numeric
from .database import Base

class pga(Base):
    __tablename__ = "pgastats"
    id = Column(Integer, primary_key=True, index=True)
    player = Column(String, unique=True, index=True)
    numofrounds = Column(Numeric)
    avgapproach = Column(Numeric)
    totalapproach= Column(Numeric)
    pergreensinreg= Column(Numeric)
    greenshitinreg= Column(Numeric)
    numholes= Column(Numeric)
