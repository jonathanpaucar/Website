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
    x=crud.get_salary(db)
    df = pd.DataFrame.from_records(x,columns=['Player','Fieldposition','Team','Salary'])

    px.defaults.width = 266
    px.defaults.height = 200

    fig = px.bar(df.head(10),x='Player', y='Salary',title='Top 10 Paid NFL Players')
    fig.update_layout( yaxis = dict( tickfont = dict(size=5)), xaxis = dict( tickfont = dict(size=5)), font=dict(size=5), margin=dict(l=0, r=0, t=0, b=0))
    top10=fig.to_html(full_html=False, include_plotlyjs='cdn')

    dfteam = df.groupby('Team')['Salary'].sum()
    dfteam = dfteam.reset_index()
    dfteam = dfteam.sort_values('Salary', ascending=False).head(10)

    fig10 = px.bar(dfteam, x='Team', y='Salary')
    fig10.update_layout( yaxis = dict( tickfont = dict(size=5)),
    xaxis = dict( tickfont = dict(size=5)),
    font=dict(size=5),
    margin=dict(l=0, r=0, t=0, b=0))
    team10 = fig10.to_html(full_html=False, include_plotlyjs='cdn')

    return templates.TemplateResponse("chart.html", {"request": request, "top10":top10, "team10":team10})
