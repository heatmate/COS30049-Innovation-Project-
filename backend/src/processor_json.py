import json
import pandas as pd
from .features import clean_code, extract_features
import re

class VulnerabilityDataProcessor:
    def __init__(self, data_path="data/raw/basic_data_3.jsonl"):
        self.data_path = data_path
        self.df = None
        self.error_df = None

    # Load JSON like file where each JSON object may be multi-line and may contain unescaped quotes/brackets 
    def load_data(self):
        rows, errors = [], []
        
        with open(self.data_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # Split objects by "}{", allowing newlines or spaces in between
        parts = re.split(r'\}\s*\{', content)
        for i, part in enumerate(parts):
            p = part.strip()
            if not p.startswith("{"):
                p = "{" + p
            if not p.endswith("}"):
                p = p + "}"

            try:
                rows.append(json.loads(p))
            except json.JSONDecodeError as e:
                errors.append({
                    "line_number": i + 1,
                    "line_content": p[:2000],  # truncated for logging
                    "error_message": str(e)
                })

        self.df = pd.DataFrame(rows)
        self.error_df = pd.DataFrame(errors)

        print(f"Loaded {len(self.df)} valid rows.")
        print(f"Found {len(self.error_df)} invalid rows.")

        return self.df, self.error_df
    
    # Group vulnerability types categorically
    def categorize_vulnerability(self, vuln_type):
        if not isinstance(vuln_type, str) or pd.isna(vuln_type):
            return 'Other'
        vuln_lower = vuln_type.lower()
        if any(term in vuln_lower for term in ['sql', 'injection', 'command']):
            return 'Injection'
        elif any(term in vuln_lower for term in ['xss', 'cross-site']):
            return 'XSS'
        elif any(term in vuln_lower for term in ['auth', 'session', 'token']):
            return 'Authentication'
        elif any(term in vuln_lower for term in ['file', 'upload', 'path']):
            return 'File_Handling'
        elif any(term in vuln_lower for term in ['config', 'cord', 'header']):
            return 'Configuration'
        else:
            return 'Other'

    # Preprocess dataset (clean, features, categories)
    def preprocess_data(self):
        if self.df is None or self.df.empty:
            raise ValueError("Data didn't load, try calling load_data() first.")
        
        self.df['clean_code'] = self.df['code_snippet'].apply(clean_code)
        # Extract the features 
        features = self.df['code_snippet'].apply(extract_features)
        self.df = pd.concat([self.df, pd.DataFrame(features.tolist())], axis=1)
        self.df['vuln_category'] = self.df['vulnerability_type'].apply(self.categorize_vulnerability)
        self.df['vul'] = 1
        print("Completed data preprocessing")
        return self.df


processor = VulnerabilityDataProcessor(data_path="data/raw/basic_data_3.jsonl")
df, error_df = processor.load_data()
print("Valid rows:", len(df))      # Should be ~9900
print("Error rows:", len(error_df)) # Should be very small or 0
df = processor.preprocess_data()
print(df.head())