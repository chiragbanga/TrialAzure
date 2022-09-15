import numpy as np
import pandas as pd
from database import engine
from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import  Session
from database import SessionLocal
import models
from pydantic import BaseModel
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

app = FastAPI()

class fishsample(BaseModel):
    Weight: float
    Length1: float
    Length2: float
    Length3: float
    Height: float
    Width: float

db = engine

sql = 'SELECT * FROM fishtraindata;'
df_fish = pd.read_sql_query(sql, db)

y = df_fish['Species']
X = df_fish.drop('Species', axis=1)
#X = df_fish[['Weight', 'Length1', 'Length2', 'Length3', 'Height', 'Width']]

logistic_model = LogisticRegression()
model = logistic_model.fit(X,y)

@app.get('/')
def fristpage():
    return{'Hello World'}

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/fishspecpred')
async def fishspecpred(parameters:fishsample, db:Session=Depends(get_db)):
    test_data_init = [[
             parameters.Weight,
             parameters.Length1,
             parameters.Length2,
             parameters.Length3,
             parameters.Height,
             parameters.Width
    ]]
    prediction = model.predict(test_data_init)[0]
    new_fishtestdata = models.fastapi_app(Weight=parameters.Weight,Length1=parameters.Length1,Length2=parameters.Length2,Length3=parameters.Length3,Height=parameters.Height,Width=parameters.Width,Species=prediction)
    db.add(new_fishtestdata)
    db.commit()
    return{'Species is': prediction}
