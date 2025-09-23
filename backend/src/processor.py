import json
import pandas as pd
from .features import clean_code, extract_features

class VulnerabilityDataProcessor:
    def __init__(self, data_path="data/basic_data_3.jsonl"):
        self.data_path = data_path
        self.df = None

    # Load basic dataset and validate JSONL 
    def load_data(self):
        rows = []
        errors = []
        
        with open(self.data_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as e:
                    errors.append({
                        "line_number": i,
                        "line_content": line.strip(),
                        "error_message": str(e)
                    })

        # DataFrames
        self.df = pd.DataFrame(rows)
        self.error_df = pd.DataFrame(errors)

        print(f"Loaded {len(self.df)} valid rows.")
        print(f"Found {len(self.error_df)} invalid rows.")

        if self.df.empty:
            print("Warning: No valid rows found. Dataset may be entirely malformed.")
            # Skip column check if no valid rows
        else:
            # Only check required columns if there are valid rows
            required_cols = ['code_snippet', 'vulnerability_type']
            missing = [col for col in required_cols if col not in self.df.columns]
            if missing:
                raise ValueError(f"Missing columns in valid rows: {missing}")

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
    def preprocess_data(self):
        if self.df is None:
            raise ValueError("Data didn't load, try calling load_data() before preprocess_data()")
        
        self.df['clean_code'] = self.df['code_snippet'].apply(clean_code)
        # Extract the features 
        features = self.df['code_snippet'].apply(extract_features)
        self.df = pd.concat([self.df, pd.DataFrame(features.tolist())], axis=1)
        self.df['vuln_category'] = self.df['vulnerability_type'].apply(self.categorize_vulnerability)
        print("Completed data preprocessing")
        return self.df
