import json
import pandas as pd
from .features import clean_code, extract_features

class VulnerabilityDataProcessor:
    def __init__(self, data_path="data/basic_data_3.jsonl"):
        self.data_path = data_path
        self.df = None
        self.error_df = None

    # Load basic dataset and validate JSONL 
    def load_data(self):
        rows, errors = [], []
        
        with open(self.data_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # First Case: a Valid JSON arrary that begins with "["" and ends with "]""
        if content.startswith("["):
            rows = json.loads(content)

        # Case 2: JSONL (one object per line)
        elif "\n" in content and content.splitlines()[0].strip().startswith("{"):
            for i, line in enumerate(content.splitlines(), 1):
                  try:
                     rows.append(json.loads(line))
                  except json.JSONDecodeError as e:
                      errors.append({
                          "line_number": i,
                          "line_content": line.strip(),
                          "error_message": str(e)
                  })

        # Case 3: The sample dataset given is multi-line and starts with "{", no valid JSON "[" 
        else:
            buffer = ""
            start_line = 0
            for i, line in enumerate(content.splitlines(), 1):
                line = line.strip()
                if not line:
                    continue
                if not buffer:
                    start_line = i 
                buffer += line
                if line.endswith("}"):
                    try:
                        rows.append(json.loads(buffer))
                    except json.JSONDecodeError as e:
                        errors.append({
                            "line_number": start_line,
                            "line_content": buffer,
                            "error_message": str(e)
                        })
                    buffer = ""

        # DataFrames
        self.df = pd.DataFrame(rows)
        self.error_df = pd.DataFrame(errors)
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


processor = VulnerabilityDataProcessor(data_path="data/basic_data_3.jsonl")
df, error_df = processor.load_data()
print("Valid rows:", len(df))      # Should be ~9900
print("Error rows:", len(error_df)) # Should be very small or 0
df = processor.preprocess_data(clean_code, extract_features)
print(df.head())