import MySQLdb as mdb
import numpy as np
import pandas as pd
import pickle
import matrix_factorization
import csv
 
 
#fetch data from database
db = mdb.connect(host="localhost" , user="root", passwd="pragya", db="test")
cursor = db.cursor()
cursor.execute("select * from user_activity;")
desc = cursor.description
results = cursor.fetchall()

for i in results:
    print i
    
ratings_df = pd.pivot_table(i, index='user_id', columns='comp_id', aggfunc=np.max)

print ratings_df