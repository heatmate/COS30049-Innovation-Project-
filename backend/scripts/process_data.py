import json
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
with open("data/basic_data_3.jsonl", "r", encoding="utf-8") as f:
    rows = [json.loads(line) for line in f]

df = pd.DataFrame(rows)
print("Sample rows:")
print(df.head())

# Clean code snippets
def clean_code(code):
    code = re.sub(r'//.*|/\*[\s\S]*?\*/', '', code)
    code = re.sub(r'\s+', ' ', code)
    return code.strip()

df['clean_code'] = df['code_snippet'].apply(clean_code)

plt.figure(figsize=(12, 6))
sns.countplot(y='vulnerability_type', data=df, order=df['vulnerability_type'].value_counts().index)
plt.title("Distribution of Vulnerability Types")
plt.xlabel("Count")
plt.ylabel("Vulnerability Type")
plt.tight_layout()
plt.show()
