from sqlalchemy.orm import Session

from . import modelspga

def get_pga_stats(db: Session):
    return db.query(modelspga.pga.player, modelspga.pga.numofrounds, modelspga.pga.avgapproach, modelspga.pga.totalapproach, modelspga.pga.pergreensinreg,
    modelspga.pga.greenshitinreg, modelspga.pga.numholes).all()
