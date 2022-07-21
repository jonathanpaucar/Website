from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session

from . import crud, models
from .database import SessionLocal, engine

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import plotly.express as px
import pandas as pd

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def welcome(request: Request, db: Session=Depends(get_db)):
    x = crud.get_salary(db)
    df =pd.DataFrame.from_records(x,columns=['Player','Fieldposition','Team','Salary'])
    df10=df.head(10)
    fig = px.bar(df10,x='Player', y='Salary',title='Top 10 Paid NFL Players')
    top10=fig.to_html(full_html=False, include_plotlyjs='cdn')
    dfteam=df.groupby('Team')['Salary'].sum()
    dfteam=dfteam.reset_index()
    dfteam=dfteam.sort_values('Salary',ascending=False).head(10)
    fig10=px.bar(dfteam,x='Team', y='Salary',title='Top 10 Paying Teams')
    team10=fig10.to_html(full_html=False, include_plotlyjs='cdn')
    return templates.TemplateResponse("chart.html", {"request":request,"top10":top10,"team10":team10})
