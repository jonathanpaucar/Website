from sqlalchemy.orm import Session

from . import models

def get_salary(db: Session):
    return db.query(models.salary.player, models.salary.fieldposition, models.salary.team).all()
