import numpy as np
import pandas as pd
import pickle
import matrix_factorization

similar_company = pickle.load(open("similar_company.dat", "rb"))

#print similar_company
# Load user ratings
#df = pd.read_csv('out.csv')
#print df
# Load movie titles
company_df = pd.read_csv('company2.csv')

#print company_df

# Convert the running list of user ratings into a matrix
#ratings_df = pd.pivot_table(df, index='user_id', columns='comp_id', aggfunc=np.max)

#print ratings_df

# Apply matrix factorization to find the latent features
#U, M = matrix_factorization.low_rank_matrix_factorization(ratings_df.as_matrix(),num_features=5,regularization_amount=1.0)

# Swap the rows and columns of product_features just so it's easier to work with
#M = np.transpose(M)
#print U
#print M
temp_df = company_df.comp_id.tolist()
#print temp_df
temp_df.sort()

 
print "enter company_id  " 
company_id = int(input())
company_index = temp_df.index(company_id)
#print company_index


 
company_information = company_df.loc[company_index]

print company_information

#print "hello"

print("We are finding company similar to this company:")
print("Company Name: {}".format(company_information.title))
 
current_features = similar_company[company_index]
print("The attributes for this company are:")
print(current_features)

# The main logic for finding similar companies:

# 1. Subtract the current company's features from every other company's features
difference = similar_company - current_features

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
print(sorted_list[['title', 'difference_score']][0:5])
