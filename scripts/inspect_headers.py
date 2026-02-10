import pandas as pd
df = pd.read_csv('Alternative CPA Pathways Survey_December 31, 2025_09.45.csv', header=None, nrows=5)
print(df.iloc[:, 11:15])
