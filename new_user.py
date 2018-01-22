import pickle
import pandas as pd

# Load prediction rules from data files
means = pickle.load(open("means.dat", "rb"))

 
company_df = pd.read_csv('company.csv', index_col='comp_id')

# Just use the average company ratings directly as the user's predicted ratings
user_ratings = means

print("company we will recommend:")

company_df['rating'] = user_ratings
company_df = company_df.sort_values(by=['rating'], ascending=False)

print(company_df[['title','rating']].head(5))