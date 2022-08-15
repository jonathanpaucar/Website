from sqlalchemy.orm import Session

from . import modelspga

def get_pga(db: Session):
    return db.query(models.pga.player, models.pga.numofrounds, models.pga.avgapproach, models.pga.totalapproach, models.pga.pergreensinreg,
    models.pga.greenshitinreg, models.pga.numholes).all()
