import MySQLdb as mdb
import numpy as np
import pandas as pd
#import pickle
import matrix_factorization
import csv
import time
start = time.time()


max = 1
min= 0
 
print "script start" 
#fetch data from database
db = mdb.connect(host="localhost" , user="root", passwd="pragya", db="test")
cursor = db.cursor()
cursor.execute("delete from similarcompany")
cursor.execute("select * from user_activity;")
desc = cursor.description

with open("user_activity.csv", "wb") as csv_file:               
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in desc])  
    csv_writer.writerows(cursor)

raw_dataset_df = pd.read_csv('user_activity.csv')

cursor.execute("select * from company_info;")
desc = cursor.description

with open("company_info.csv", "wb") as csv_file:               
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in desc]) # write headers
    csv_writer.writerows(cursor)
company_df = pd.read_csv('company_info.csv')
# Convert the running list of user ratings into a matrix
ratings_df = pd.pivot_table(raw_dataset_df, index='user_id', columns='comp_id', aggfunc=np.max)
#print max(ratings_df)
 
normalized_ratings, means = matrix_factorization.normalize_ratings(ratings_df.as_matrix())

 
U, M = matrix_factorization.low_rank_matrix_factorization(normalized_ratings,num_features=5, regularization_amount=1.1)

#U, M = matrix_factorization.low_rank_matrix_factorization(ratings_df.as_matrix(),num_features=5,regularization_amount=1.0)

#predicted_ratings = np.matmul(U, M)
M = np.transpose(M)
 
temp_df = company_df.comp_id.tolist()
temp_df.sort()

for i in range(len(company_df)):
    company_id = temp_df[i]
    #print company_id
    company_index= temp_df.index(company_id)
    company_information = company_df.loc[company_index]
    #print company_information
    current_features= M[company_index]
    #print current_features
    difference = M - current_features
    absolute_difference = np.abs(difference)
    total_difference = np.sum(absolute_difference, axis=1)
    #total_difference = round(total_difference, 5)
    company_df['difference_score'] = total_difference
    sorted_list = company_df.sort_values('difference_score')
    #print sorted_list
    temp = sorted_list.comp_id.tolist()
    #print len(temp)
    temp1 = sorted_list.difference_score.tolist()
    
    for t in range(len(temp1)):
        similarity_score = ((max-temp1[t])/(max-min))*100
        similarity_score=round(similarity_score,2)
        if similarity_score >=99.98:
            cursor.execute("""INSERT INTO `similarcompany` VALUES (%s,%s,%s) """,(company_id,temp[t],similarity_score))
     
db.commit()
cursor.close()
db.close()

#predicted_ratings = predicted_ratings + means

 
#pickle.dump(U, open("user_features.dat", "wb"))
#pickle.dump(M, open("product_features.dat", "wb"))
#pickle.dump(predicted_ratings, open("predicted_ratings.dat", "wb" ))
#pickle.dump(means, open("means.dat", "wb" ))

print  "Script complete "
print 'It took', time.time()-start, 'seconds.'