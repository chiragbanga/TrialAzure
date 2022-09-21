import numpy as np
import pandas as pd
from database import engine
from fastapi import FastAPI,Request,Form, status
from fastapi import Depends
from database import SessionLocal
import models
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import  Session
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

app = FastAPI()

models.Base.metadata.create_all(engine)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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

logistic_model = LinearDiscriminantAnalysis() #LogisticRegression(C=0.0001, max_iter=1000, penalty='none', solver='saga')
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

@app.get("/frontend", response_class=HTMLResponse)
async def read_item(request: Request):
    weight = ""
    length1=""
    length2=''
    length3=''
    height=''
    width=''
    species=''
    return templates.TemplateResponse("item.html",context={'request': request, 'weight': weight,'length1':length1,'length2':length2,'length3':length3,'height':height,'width':width,'species':species})

@app.post("/frontend")
def form_post(request: Request, Weight: float = Form(...),Length1:float=Form(...),Length2:float=Form(...),Length3:float=Form(...),Height:float=Form(...),Width:float=Form(...), db1:Session=Depends(get_db)):
    weight =Weight
    length1=Length1
    length2=Length2
    length3=Length3
    height=Height
    width=Width
    test_data = [[weight, length1, length2,length3, height, width]]
    class_idx = logistic_model.predict(test_data)[0]
    species = class_idx
    new_fishtestdata = models.fastapi_app(Weight=weight,Length1=length1,Length2=length2,Length3=length3,Height=height,Width=width,Species=species)
    db1.add(new_fishtestdata)
    db1.commit()
    return templates.TemplateResponse('item.html', context={'request': request, 'weight': weight,'length1':length1,'length2':length2,'length3':length3,'height':height,'width':width,'species':species})

#@app.post('/fishspecpred')
#sync def fishspecpred(parameters:fishsample,status_code=status.HTTP_201_CREATED):
#    test_data_init = [[
#             parameters.Weight,
#             parameters.Length1,
#             parameters.Length2,
#             parameters.Length3,
#             parameters.Height,
#             parameters.Width
#    ]]
#    prediction = model.predict(test_data_init)[0]
#    new_fishtestdata = models.fastapi_app(Weight=parameters.Weight,Length1=parameters.Length1,Length2=parameters.Length2,Length3=parameters.Length3,Height=parameters.Height,Width=parameters.Width,Species=prediction)
#    db.add(new_fishtestdata)
#    db.commit()
#    return{'Species is': prediction}
