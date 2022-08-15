from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session

from . import crudpga, modelspga
from .database import SessionLocal, engine

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import plotly.express as px
import pandas as pd

modelspga.Base.metadata.create_all(bind=engine)
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
    x=crud.get_totalapproach(db)
    df = pd.DataFrame.from_records(x,columns=['Player','numofrounds','avgapproach','totalapproach','pergreensinreg','greenshitinreg','numholes'])
    px.defaults.width = 266
    px.defaults.height = 200

    fig = px.bar(df.head(10),x='Player', y='totalapproach',color='numofrounds').update_xaxes(categoryorder="total descending")
    fig.update_layout(yaxis = dict(tickfont = dict(size=5)),xaxis = dict(tickfont = dict(size=5)),font=dict(size=5),margin=dict(l=0, r=0, t=0, b=0))
    top10=fig.to_html(full_html=False, include_plotlyjs='cdn')

    dfavgapproach = df.groupby('avgapproach')['totalapproach'].sum()
    dfavgapproach = dfavgapproach.reset_index()
    dfavgapproach = dfavgapproach.sort_values('totalapproach', ascending=False).head(10)

    fig10 = px.bar(dfavgapproach, x='avgapproach', y='totalapproach')
    fig10.update_layout(yaxis = dict(tickfont = dict(size=5)),xaxis = dict(tickfont = dict(size=5)),font=dict(size=5),margin=dict(l=0, r=0, t=0, b=0))
    avgapproach10 = fig10.to_html(full_html=False, include_plotlyjs='cdn')

    dfavgapproach = df.loc[df['avgapproach'].isin(dfavgapproach.avgapproach)]
    figavgapproach = px.bar(dfavgapproach, x='avgapproach', y='totalapproach',color='numofrounds').update_xaxes(categoryorder="total descending")
    figavgapproach.update_layout(yaxis = dict(tickfont = dict(size=5)),xaxis = dict(tickfont = dict(size=5)),font=dict(size=5),margin=dict(l=0, r=0, t=0, b=0))
    avgapproachtotalapproach = figavgapproach.to_html(full_html=False, include_plotlyjs='cdn')

    pos10 = dfavgapproach.groupby('numofrounds')['totalapproach'].mean().sort_values(ascending=False).head(10)
    pos10 = pos10.reset_index()
    figpos = px.box(dfavgapproach.loc[dfavgapproach['numofrounds'].isin(pos10.numofrounds)],x='numofrounds', y='totalapproach')
    figpos.update_layout(yaxis = dict(tickfont = dict(size=5)),xaxis = dict(tickfont = dict(size=5)),font=dict(size=5),margin=dict(l=0, r=0, t=0, b=0))
    postotalapproach = figpos.to_html(full_html=False, include_plotlyjs='cdn')

    bottom10 = df.groupby('avgapproach')['totalapproach'].sum()
    bottom10 = bottom10.reset_index()
    bottom10 = dfavgapproach.sort_values('totalapproach', ascending=False).tail(10)
    dfavgapproach = df.loc[df['avgapproach'].isin(bottom10.avgapproach)]

    pos10 = dfavgapproach.groupby('numofrounds')['totalapproach'].mean().sort_values(ascending=False).head(10)
    pos10 = pos10.reset_index()
    figpos2 = px.box(dfavgapproach.loc[dfavgapproach['numofrounds'].isin(pos10.numofrounds)],x='numofrounds', y='totalapproach', color_discrete_sequence=['red'])
    figpos2.update_layout(yaxis = dict(tickfont = dict(size=5)),xaxis = dict(tickfont = dict(size=5)),font=dict(size=5),margin=dict(l=0, r=0, t=0, b=0))
    postotalapproach2 = figpos2.to_html(full_html=False, include_plotlyjs='cdn')

    dfavgapproach = df.groupby('numofrounds')['totalapproach'].mean()
    dfavgapproach = dfavgapproach.reset_index()
    dfavgapproach = dfavgapproach.sort_values('totalapproach', ascending=False)

    figpie = px.pie(dfavgapproach, values='totalapproach', names='numofrounds')
    figpie.update_layout(yaxis = dict(tickfont = dict(size=5)),xaxis = dict(tickfont = dict(size=5)),font=dict(size=5),margin=dict(l=0, r=0, t=0, b=0))
    pospie = figpie.to_html(full_html=False, include_plotlyjs='cdn')

    return templates.TemplateResponse("chart.html", {"request": request, "top10":top10, "avgapproach10":avgapproach10,"avgapproachtotalapproach":avgapproachtotalapproach,"postotalapproach":postotalapproach,"postotalapproach2":postotalapproach2,"pospie":pospie})
