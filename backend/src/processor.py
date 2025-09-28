import json
import re
import pandas as pd
from features import clean_code, extract_features

class VulnerabilityDataProcessor:
    def __init__(self, data_path="../data/basic_data_3.jsonl"):
        self.data_path = data_path
        self.df = None
        self.error_df = None

    # Load basic dataset and validate JSONL 
    def load_data(self):
        rows, errors = [], []
        
        with open(self.data_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # Split by "}{", allowing any whitespace/newline between them
        parts = re.split(r'\}\s*\{', content)
        for i, part in enumerate(parts):
            p = part.strip()
            # re-add braces that were removed by split
            if not p.startswith("{"):
                p = "{" + p
            if not p.endswith("}"):
                p = p + "}"
            try:
                # parse this chunk
                rows.append(json.loads(p))
            except json.JSONDecodeError as e:
                errors.append({
                    "line_number": i + 1,
                    "line_content": p[:2000],   # truncate long blocks for log
                    "error_message": str(e)
                })

        self.df = pd.DataFrame(rows)
        self.error_df = pd.DataFrame(errors)
        print(f"Loaded {len(self.df)} valid rows.")
        print(f"Found {len(self.error_df)} invalid rows.")
        return self.df, self.error_df
    
    # Group vulnerability types categorically
    def categorize_vulnerability(self, vuln_type):
        vuln_lower = vuln_type.lower()
        if any(term in vuln_lower for term in ['sql', 'injection', 'command']):
            return 'Injection'
        elif any(term in vuln_lower for term in ['xss', 'cross-site']):
            return 'XSS'
        elif any(term in vuln_lower for term in ['auth', 'session', 'token']):
            return 'Authentification'
        elif any(term in vuln_lower for term in ['file', 'upload', 'path']):
            return 'File_Handling'
        elif any(term in vuln_lower for term in ['config', 'cord', 'header']):
            return 'Configuration'
        else:
            return 'Other'

    # Preprocess dataset (clean, features, categories)
    def preprocess_data(self, clean_code, extract_features):
        if self.df is None or self.df.empty:
            raise ValueError("Data didn't load, try calling load_data() before preprocess_data()")
        
        self.df['clean_code'] = self.df['code_snippet'].apply(clean_code)
        # Extract the features 
        features = self.df['code_snippet'].apply(extract_features)
        self.df = pd.concat([self.df, pd.DataFrame(features.tolist())], axis=1)
        self.df['vuln_category'] = self.df['vulnerability_type'].apply(self.categorize_vulnerability)
        print("Completed data preprocessing")
        return self.df
    

if __name__ == "__main__":
    processor = VulnerabilityDataProcessor(data_path="../data/basic_data_3.jsonl")
    df, error_df = processor.load_data()
    print("Valid rows:", len(df))
    print("Error rows:", len(error_df))
    if len(df):
        df = processor.preprocess_data(clean_code, extract_features)
        print(df.head())