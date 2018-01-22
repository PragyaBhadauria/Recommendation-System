import MySQLdb as mdb
import pickle
import pandas as pd
import numpy as np
import csv

# Load prediction rules from data files
U = pickle.load(open("user_features.dat", "rb"))
M = pickle.load(open("product_features.dat", "rb"))
predicted_ratings = pickle.load(open("predicted_ratings.dat", "rb"))


print U
#print predicted_ratings
raw_dataset_df = pd.read_csv('out.csv')

#to know the index value of user_id
ratings_df = pd.pivot_table(raw_dataset_df, index='user_id', columns='comp_id', aggfunc=np.max)

"""db = mdb.connect(host="localhost" , user="root", passwd="pragya", db="test")
cursor = db.cursor()
cursor.execute("select * from company_info;")
desc = cursor.description

with open("company2.csv", "wb") as csv_file:               
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in desc]) # write headers
    csv_writer.writerows(cursor)"""


company_df = pd.read_csv('company2.csv', index_col='comp_id')

print("Enter a user_id to get recommendations:")
user = float(input())
user_id_to_search= ratings_df.index.get_loc(user)

print("company previously reviewed by user_id - {}:".format(user))

reviewed_company_df = raw_dataset_df[raw_dataset_df['user_id'] == user]
reviewed_company_df = reviewed_company_df.join(company_df, on='comp_id')

print(reviewed_company_df[['title', 'value']])

print("company we will recommend:")

user_ratings = predicted_ratings[user_id_to_search]

company_df['rating'] = user_ratings

company_df = company_df.sort_values(by=['rating'], ascending=False)

print(company_df[['title', 'rating']].head(5))