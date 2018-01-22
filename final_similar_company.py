import numpy as np
import pandas as pd
import pickle
import MySQLdb as mdb
 
similar_company = pickle.load(open("similar_company.dat", "rb"))

db = mdb.connect(host="localhost" , user="root", passwd="pragya", db="test")
cursor = db.cursor()
cursor.execute("delete from similarcompany")
#print similar_company
#print np.shape(similar_company)
company_df = pd.read_csv('company2.csv')
l= len(company_df)
#print l
#to know index of company_id
temp_df = company_df.comp_id.tolist()
temp_df.sort()

for i in range(l):
    company_id = temp_df[i]
    #print company_id
    company_index= temp_df.index(company_id)
    company_information = company_df.loc[company_index]
    #print company_information
    current_features= similar_company[company_index]
    #print current_features
    difference = similar_company - current_features
    absolute_difference = np.abs(difference)
    total_difference = np.sum(absolute_difference, axis=1)
    company_df['difference_score'] = total_difference
    sorted_list = company_df.sort_values('difference_score')
    #print sorted_list
    temp = sorted_list.comp_id.tolist()
    #print len(temp)
    temp1 = sorted_list.difference_score.tolist()
    #print len(temp1)
    
        #print temp[k]
        #cursor.execute("""INSERT INTO `similarcompany` VALUES (%s,%s,%s) """,(company_id,temp[k],temp1[k]))
    for t in range(len(temp1)):
        #print "start"
        if temp1[t] <= 0.00015:
            #print temp1[t]
            
            cursor.execute("""INSERT INTO `similarcompany` VALUES (%s,%s,%s) """,(company_id,temp[t],temp1[t]))
            #print "end"
            
        
        
    
            
    #print temp1[1]
   
    #for k in range(1660):
        #print temp[k]
        #cursor.execute("""INSERT INTO `similarcompany` VALUES (%s,%s,%s) """,(company_id,temp[k],temp1[k]))
    

#print sorted_list
    #print("The five most similar companies are:")

#query = "insert into"    
"""for k in range(5):
    print temp[k]"""
     
db.commit()
cursor.close()
db.close()
print "bye"
    
"""top_similar_company = sorted_list[['comp_id']][0:5]
print top_similar_company
r = len(top_similar_company)
for j in range(r):
    print top_similar_company[j]
         

#print temp_df[1]"""
"""print "enter company_id  " 
company_id = int(input())
company_index = temp_df.index(company_id)
company_information = company_df.loc[company_index]
print company_information

print("We are finding company similar to this company:")
print("Company Name: {}".format(company_information.title))
 
current_features = similar_company[company_index]
print("The attributes for this company are:")

#logic for finding similar companies:

# 1. Subtract the current company's features from every other company's features
difference = similar_company - current_features

print difference

# 2. Take the absolute value of that difference (so all numbers are positive)
absolute_difference = np.abs(difference)

# 3. Each company has 5 features. Sum those 5 features to get a total 'difference score' for each company
total_difference = np.sum(absolute_difference, axis=1)

# 4. Create a new column in the company list with the difference score for each company
company_df['difference_score'] = total_difference

# 5. Sort the company list by difference score, from least different to most different
sorted_list = company_df.sort_values('difference_score')

# 6. Print the result, showing the 5 most similar company  
print("The five most similar companies are:")
print(sorted_list[['comp_id','title', 'difference_score']][0:5])"""


