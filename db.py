import MySQLdb as mdb
import pickle
import pandas as pd
import numpy as np
import csv

# Load prediction rules from data files
U = pickle.load(open("user_features.dat", "rb"))
M = pickle.load(open("product_features.dat", "rb"))
predicted_ratings = pickle.load(open("predicted_ratings.dat", "rb"))

#print np.shape(predicted_ratings)
raw_dataset_df = pd.read_csv('out.csv')

#print raw_dataset_df
#to know the index value of user_id
ratings_df = pd.pivot_table(raw_dataset_df, index='comp_id', columns='user_id', aggfunc=np.max)
#print ratings_df

db = mdb.connect(host="localhost" , user="root", passwd="pragya", db="recommendation")
cursor = db.cursor()
cursor.execute("select * from company;")
desc = cursor.description

with open("company2.csv", "wb") as csv_file:              # Python 2 version
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in desc]) # write headers
    csv_writer.writerows(cursor)


#print raw_dataset_df
company_df = pd.read_csv('company2.csv', index_col='comp_id')



#print company_df

print("Enter a company_id to get recommendations:")
#print("Enter a comp_id to get recommendations:")
user = int(input())
user_id_to_search= ratings_df.index.get_loc(user)


#_user = predicted_ratings.iloc[user_id_to_search]
#user = pd.Index.get_loc(user_id_to_search)

#user = predicted_ratings.index(user_id_to_search)

#print user_id_to_search
#print("company previously reviewed by user_id {}:".format(user_id_to_search))

reviewed_company_df = raw_dataset_df[raw_dataset_df['comp_id'] == user]
reviewed_company_df = reviewed_company_df.join(company_df, on='comp_id')

print(reviewed_company_df[['title', 'value']])

print("company we will recommend:")

#print predicted_ratings[19]

user_ratings = predicted_ratings[user_id_to_search-1]

#print user_ratings
company_df['rating'] = user_ratings

#print company_df['rating']
company_df = company_df.sort_values(by=['rating'], ascending=False)

print(company_df[['title', 'rating']].head(5))




