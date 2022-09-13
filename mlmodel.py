import numpy as np
import pandas as pd
import mysql.connector
from databaseconnection import engine, username_db, password_db, host_server, db_server_port, database_name
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

db = engine

connection = mysql.connector.connect(
    user=username_db, password=password_db,
    host=host_server, port=3306,
    database=database_name
)
c = connection.cursor()

sql = "SELECT * FROM fishtraindata;"
df_fish = pd.read_sql_query(sql, db)

y = df_fish['Species']
X = df_fish.drop('Species', axis=1)
#X = df_fish[['Weight', 'Length1', 'Length2', 'Length3', 'Height', 'Width']]

logistic_model = LogisticRegression()
model = logistic_model.fit(X,y)

pickle.dump(logistic_model, open('fish_model.pkl', 'wb'))