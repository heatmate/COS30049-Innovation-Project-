import json
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

class VulnerabilityDataProcessor:
    def __init__(self, data_path="data/basic_data_3.jsonl"):
        self.data_path = data_path
        self.df = None 
        self.vectorizer = None
        self.label_encoder = None
        self.models = {}

    # Load basic dataset and validate JSONL 
    def load_data(self):
        rows = []
        with open("data/basic_data_3.jsonl", "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Skipping line {i}: {e}")

    # Create a dataframe of rows 
        self.df = pd.DataFrame(rows)
        print(f"Loaded {len(self.df)} valid rows.")
        print("Columns in dataframe:", self.df.columns.tolist())

        if self.df.empty:
            raise ValueError("No Valid Data Found.")

        required_cols = ['code_snippet', 'vulnerability_type']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Missing columns: {missing_cols}")
    
        return self.df

    # Clean and normalise the code snippets for easier processing
    def clean_code(self, code):
        if pd.isna(code):
            return ""
        # Removes all comments
        code = re.sub(r'//.*|/\*[\s\S]*?\*/', '', str(code))
        # Removes the extra whitespace
        code = re.sub(r'\s+', ' ', code)
        # Remove the common boilerplate
        code = re.sub(r'require\([\'"][\w\-/\.]+[\'"]\)', 'require()', code)
        return code.strip()

    def extract_features(self, code):
        if pd.isna(code):
            return {}
        
        code_str = str(code)
        features = {
            'has_user_input': any(keyword in code_str.lower() for keyword in
                                   ['req.', 'input', 'param', 'query', 'body']),
            'has_db_operation': any(keyword in code_str.lower() for keyword in
                                    ['query', 'exec', 'select', 'insert', 'update', 'complete']),
            'has_file_operation': any(keyword in code_str.lower() for keyword in
                                      ['readfile', 'writefile', 'open', 'fs.']),
            'has_eval': any(keyword in code_str.lower() for keyword in
                            ['exec', 'eval', 'system', 'shell']),
            'code_length': len(code_str),
            'has_validation': any(keyword in code_str.lower() for keyword in
                                  ['validate', 'sanitize', 'escape', 'filter']),
            'has_quotes': "'" in code_str or '"' in code_str,
            'has concatenation': '+' in code_str or '${' in code_str or '%s' in code_str

        }
        return features

    df['clean_code'] = df['code_snippet'].apply(clean_code)

    print("\nSample Cleaned Code:")
    print(df[['code_snippet', 'clean_code']].head())

    # Visualize the vulnerability types 
    plt.figure(figsize=(12, 6))
    sns.countplot(y='vulnerability_type',
        data=df,
        order=df['vulnerability_type'].value_counts().index,
        palette='viridis'
    )
plt.title("Distribution of Vulnerability Types")
plt.xlabel("Count")
plt.ylabel("Vulnerability Type")
plt.tight_layout()
plt.show()
