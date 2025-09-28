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

        # Insert a newline between glued objects (} immediately followed by {, possibly with whitespace)
        content = re.sub(r'\}\s*\{', '}\n{', content)

        # Split into chunks at newlines followed by '{'
        chunks = re.split(r'\n(?=\{)', content)
        # 2. Escape quotes inside code_snippet without using lookbehind
        def escape_inner_quotes(match):
            inner = match.group(1)
            inner_escaped = inner.replace('"', r'\"')
            return f'"code_snippet": "{inner_escaped}"'
        
        for i, chunk in enumerate(chunks):
            chunk_fixed = chunk

            # Attempt to fix common JSON issues
            # 1. Replace unescaped backslashes
            chunk_fixed = chunk_fixed.replace('\\', '\\\\')
            chunk_fixed = re.sub(r'"code_snippet"\s*:\s*"([^"]*?)"', escape_inner_quotes, chunk_fixed)

            # 3. Remove control characters that break JSON
            chunk_fixed = re.sub(r'[\x00-\x1f]', '', chunk_fixed)

            try:
                rows.append(json.loads(chunk_fixed))
            except json.JSONDecodeError as e:
                errors.append({
                    "line_number": i + 1,
                    "line_content": chunk[:2000],
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

        # Inspect the invalid JSON chunks
    if not error_df.empty:
        for i, row in error_df.iterrows():
            print(f"Chunk {row['line_number']} failed:")
            print(row['line_content'][:500])  # first 500 chars to keep output manageable
            print("Error:", row['error_message'])
            print("--------")

    if len(df):
        df = processor.preprocess_data(clean_code, extract_features)
        print(df.head())