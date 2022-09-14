from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import  Session
from databaseconnection import SessionLocal
import datamodel
from pydantic import BaseModel
import pickle
import mlmodel

app = FastAPI()

pickled_model = pickle.load(open('fish_model.pkl', 'rb'))

class fishsample(BaseModel):
    Weight: float
    Length1: float
    Length2: float
    Length3: float
    Height: float
    Width: float

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
    prediction = pickled_model.predict(test_data_init)[0]
    new_fishtestdata = datamodel.database1(Weight=parameters.Weight,Length1=parameters.Length1,Length2=parameters.Length2,Length3=parameters.Length3,Height=parameters.Height,Width=parameters.Width,Species=prediction)
    db.add(new_fishtestdata)
    db.commit()
    return{'Species is': prediction}