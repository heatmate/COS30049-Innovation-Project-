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
        # With open will close the file after
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
        self.df['clean_code'] = self.df['code_snippet'].apply(clean_code)
        # Extract the features 
        features = self.df['code_snippet'].apply(extract_features)
        self.df = pd.concat([self.df, pd.DataFrame(features.tolist())], axis=1)
        self.df['vuln_category'] = self.df['vulnerability_type'].apply(self.categorize_vulnerability)
        print("Completed data preprocessing")
        return self.df
                                  
   

    # Prepare data or machine learning
    def prepare_ml_data(self):
        # USING TF-IDF for text features 
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )

        text_features = self.vectorizer.fit_transform(self.df['clean_code'])
        feature_cols = ['has_user_input', 'has_db_operation', 'has_file_operation', 'has_eval', 
                        'code_length', 'has_validation', 'has_quotes','has_concatenation']
        numerical_features = self.df[feature_cols].fillna(0).astype(int)

    # Combine features 
        X = hstack([text_features, numerical_features.values])     

    #Encode the labels now 
        self.label_encoder = LabelEncoder()
        y = self.label_encoder.fit_transform(self.df['vuln_category'])   

        return X, y 

    # Train MULTIPLE ML models
    def train_models