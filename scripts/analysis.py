import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Ensure output directory exists
os.makedirs('outputs', exist_ok=True)

# Load the data
file_path = 'Alternative CPA Pathways Survey_December 31, 2025_09.45.csv'
print(f"Loading data from {file_path}...")
df = pd.read_csv(file_path, header=0)

# Extract question text for reference (Row 0 in df which is Line 2 in file)
question_text = df.iloc[0]

# Actual data starts after the ImportId row (Row 1 in df which is Line 3 in file)
# So we slice from index 2 onwards
df_data = df.iloc[2:].copy()

print(f"Total respondents after filtering headers: {len(df_data)}")

# Filter for Undergrads and Grads
undergrads = df_data[df_data['Q27'] == 'Undergraduate'].copy()
grads = df_data[df_data['Q27'] == 'Graduate'].copy()

print(f"Undergraduates: {len(undergrads)}")
print(f"Graduates: {len(grads)}")

# --- Task A: The "Cannibalization" Risk (Undergraduate Pipeline) ---
print("\n--- Task A: Cannibalization Risk ---")

# Map Likert Scales
# Q29 (CPA Likelihood)
q29_mapping = {
    'Very unlikely': 1,
    'Somewhat unlikely': 2,
    'Neither likely nor unlikely': 3,
    'Somewhat likely': 4,
    'Very likely': 5
}
undergrads['Q29_numeric'] = undergrads['Q29'].map(q29_mapping)

# Q52 (Impact on Desire)
q52_mapping = {
    'Significantly decreased desire': -2,
    'Decreased desire': -1,
    'No change in desire': 0, # Corrected string
    'Increased desire': 1,
    'Significantly increased desire': 2
}
undergrads['Q52_numeric'] = undergrads['Q52'].map(q52_mapping)

# Drop NaNs in relevant columns for plotting
undergrads_a = undergrads.dropna(subset=['Q29_numeric', 'Q52_numeric'])

# Group by Q29 and calculate distribution of Q52
# We want a 100% stacked bar chart
ct = pd.crosstab(undergrads_a['Q29_numeric'], undergrads_a['Q52_numeric'], normalize='index') * 100

# Plotting
plt.figure(figsize=(10, 6))
# Using a colormap that highlights negative (red) to positive (green/blue)
# Q52 values are -2, -1, 0, 1, 2.
# We want to map these to colors.
ct.plot(kind='bar', stacked=True, colormap='RdBu', ax=plt.gca())

plt.title('Impact of Alternative CPA Pathways on Desire to Pursue CPA\nby Initial Likelihood (Undergraduates)')
plt.xlabel('CPA Likelihood (1=Very Unlikely, 5=Very Likely)')
plt.ylabel('Percentage of Respondents')
plt.legend(title='Impact on Desire', bbox_to_anchor=(1.05, 1), loc='upper left',
           labels=['Significantly Decreased (-2)', 'Decreased (-1)', 'No Change (0)', 'Increased (+1)', 'Significantly Increased (+2)'])
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('outputs/task_a_cannibalization.png')
plt.close()
print("Saved outputs/task_a_cannibalization.png")

# Calculate Cannibalization Rate
# Percentage of "Very Likely" (5) CPA students who selected "Decreased" (-1) or "Significantly Decreased" (-2) desire.
very_likely_group = undergrads_a[undergrads_a['Q29_numeric'] == 5]
total_very_likely = len(very_likely_group)
cannibalized = very_likely_group[very_likely_group['Q52_numeric'].isin([-1, -2])]
cannibalization_count = len(cannibalized)

cannibalization_rate = (cannibalization_count / total_very_likely) * 100 if total_very_likely > 0 else 0

print(f"Total 'Very Likely' students: {total_very_likely}")
print(f"Cannibalized students: {cannibalization_count}")
print(f"Cannibalization Rate: {cannibalization_rate:.2f}%")


# --- Task B: The "Value Proposition" (Graduate Student Perception) ---
print("\n--- Task B: Value Proposition ---")

# Columns Q24_1 to Q24_6
q24_cols = ['Q24_1', 'Q24_2', 'Q24_3', 'Q24_4', 'Q24_5', 'Q24_6']

# Convert to numeric
for col in q24_cols:
    grads[col] = pd.to_numeric(grads[col], errors='coerce')

# Calculate Mean Rank
mean_ranks = grads[q24_cols].mean()

# Mapping labels
q24_labels = {
    'Q24_1': 'CPA Exam Prep',
    'Q24_2': 'Networking',
    'Q24_3': 'Faculty Interaction',
    'Q24_4': 'Technical Skills',
    'Q24_5': 'Soft Skills',
    'Q24_6': 'Recruiting/Internships'
}
mean_ranks.index = mean_ranks.index.map(q24_labels)

# Sort: Lower Number = Higher Importance
mean_ranks_sorted = mean_ranks.sort_values(ascending=True)

print("Mean Ranks (Lower is Better/Harder to Replace):")
print(mean_ranks_sorted)

# Plotting
plt.figure(figsize=(10, 6))
# Invert for display so best rank (lowest number) is at top
mean_ranks_sorted.iloc[::-1].plot(kind='barh', color='skyblue')

plt.title('Graduate Student Value Proposition: Mean Rank of Program Aspects')
plt.xlabel('Mean Rank')
plt.annotate('Lower Score = Harder to Replace', xy=(0.5, -0.15), xycoords='axes fraction', ha='center', fontsize=10, style='italic')
plt.tight_layout()
plt.savefig('outputs/task_b_value_proposition.png')
plt.close()
print("Saved outputs/task_b_value_proposition.png")

# Identify top 2 "Hardest to Replace" aspects
top_2 = mean_ranks_sorted.head(2)
print("\nTop 2 Hardest to Replace aspects:")
for item, rank in top_2.items():
    print(f"- {item} (Mean Rank: {rank:.2f})")

# Write findings to a temporary file for the notebook creator to read (optional, or just hardcode in notebook creator)
with open('outputs/findings.txt', 'w') as f:
    f.write(f"Cannibalization Rate: {cannibalization_rate:.2f}%\n")
    f.write("Top 2 Hardest to Replace:\n")
    for item, rank in top_2.items():
        f.write(f"- {item} ({rank:.2f})\n")

print("Analysis complete.")
