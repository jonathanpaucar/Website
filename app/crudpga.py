from sqlalchemy.orm import Session

from . import modelspga

def get_pgastats(db: Session):
    return db.query(modelspga.pgastats.player, modelspga.pgastats.numofrounds, modelspga.pgastats.avgapproach, modelspga.pgastats.totalapproach, modelspga.pgastats.pergreensinreg,
    modelspga.pgastats.greenshitinreg, modelspga.pgastats.numholes).all()
