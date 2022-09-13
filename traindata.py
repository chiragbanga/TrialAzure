import pandas as pd
#import mysql.connector
#from databaseconnection import engine, username_db, password_db, host_server, db_server_port, database_name

#db = engine

#connection = mysql.connector.connect(
#    user=username_db, password=password_db,
#    host=host_server, port=3306,
#    database=database_name
#)
#c = connection.cursor()

#sql = "SELECT * FROM fishtraindata;"
#df_fish = pd.read_sql_query(sql, db)

df_fish = pd.read_csv("Fish.csv")