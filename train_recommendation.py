import MySQLdb as mdb
import numpy as np
import pandas as pd
import pickle
import matrix_factorization
import csv
 
 
#db = mdb.connect(host="localhost" , user="root", passwd="pragya", db="recommendation")
db = mdb.connect(host="localhost" , user="root", passwd="pragya", db="test")
cursor = db.cursor()
cursor.execute("select * from user_activity;")
desc = cursor.description

with open("out.csv", "wb") as csv_file:              # Python 2 version
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in desc]) # write headers
    csv_writer.writerows(cursor)

raw_dataset_df = pd.read_csv('out.csv')

print raw_dataset_df

# Convert the running list of user ratings into a matrix
ratings_df = pd.pivot_table(raw_dataset_df, index='user_id', columns='comp_id', aggfunc=np.max)
print ratings_df
#print("Enter a user_id to get recommendations:")
#user = float(input())
#print ratings_df.index.get_loc(user)


normalized_ratings, means = matrix_factorization.normalize_ratings(ratings_df.as_matrix())

 
U, M = matrix_factorization.low_rank_matrix_factorization(normalized_ratings,
                                                                    num_features=5,
                                                                    regularization_amount=1.1)

#S = matrix_factorization.low_rank_matrix_factorization(ratings_df.as_matrix(),num_features=5,regularization_amount=1.0)
#print U

T, S = matrix_factorization.low_rank_matrix_factorization(ratings_df.as_matrix(),num_features=5,regularization_amount=1.0)

print S

predicted_ratings = np.matmul(U, M)

#print predicted_ratings

similar_company = np.transpose(S)


predicted_ratings = predicted_ratings + means

 
pickle.dump(U, open("user_features.dat", "wb"))
pickle.dump(M, open("product_features.dat", "wb"))
pickle.dump(predicted_ratings, open("predicted_ratings.dat", "wb" ))
pickle.dump(similar_company, open("similar_company.dat", "wb" ))
pickle.dump(means, open("means.dat", "wb" ))
print  "bye"