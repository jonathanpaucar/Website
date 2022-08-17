from sqlalchemy import Column, Float, String, Integer, Numeric
from .database import Base

class pga(Base):
    __tablename__ = "pga_stats"
    player = Column(String, unique=True, index=True)
    numofrounds = Column(Numeric)
    avgapproach = Column(Numeric)
    totalapproach= Column(Numeric)
    pergreensinreg= Column(Numeric)
    greenshitinreg= Column(Numeric)
    numholes= Column(Numeric)
