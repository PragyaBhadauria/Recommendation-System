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

with open("out.csv", "wb") as csv_file:               
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in desc])  
    csv_writer.writerows(cursor)

raw_dataset_df = pd.read_csv('out.csv')

cursor.execute("select * from company_info;")
desc = cursor.description

with open("company2.csv", "wb") as csv_file:               
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in desc]) # write headers
    csv_writer.writerows(cursor)

# Convert the running list of user ratings into a matrix
ratings_df = pd.pivot_table(raw_dataset_df, index='user_id', columns='comp_id', aggfunc=np.max)
print ratings_df
 
normalized_ratings, means = matrix_factorization.normalize_ratings(ratings_df.as_matrix())

 
U, M = matrix_factorization.low_rank_matrix_factorization(normalized_ratings,num_features=5, regularization_amount=1.1)

#print M
T, S = matrix_factorization.low_rank_matrix_factorization(ratings_df.as_matrix(),num_features=5,regularization_amount=1.0)

predicted_ratings = np.matmul(U, M)

similar_company = np.transpose(S)

#print similar_company

predicted_ratings = predicted_ratings + means

 
pickle.dump(U, open("user_features.dat", "wb"))
pickle.dump(M, open("product_features.dat", "wb"))
pickle.dump(predicted_ratings, open("predicted_ratings.dat", "wb" ))
pickle.dump(similar_company, open("similar_company.dat", "wb" ))
pickle.dump(means, open("means.dat", "wb" ))

print  "Script complete "