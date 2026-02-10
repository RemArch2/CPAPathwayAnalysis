import pandas as pd

# Load the data
file_path = 'Alternative CPA Pathways Survey_December 31, 2025_09.45.csv'
df = pd.read_csv(file_path, header=0)
# Drop the question text row
df_data = df.iloc[1:].copy()

print("Q29 unique values:")
print(df_data['Q29'].unique())

print("\nQ52 unique values:")
print(df_data['Q52'].unique())

print("\nQ27 unique values:")
print(df_data['Q27'].unique())
