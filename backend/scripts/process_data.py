import json
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
import os
from scipy.sparse import hstack

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
            'has_concatenation': '+' in code_str or '${' in code_str or '%s' in code_str

        }
        return features
    
    def preprocess_data(self):
        self.df['clean_code'] = self.df['code_snippet'].apply(self.clean_code)

        # Extract the features 
        feature_dicts = self.df['clean_code'].apply(self.extract_features)
        feature_df = pd.DataFrame(feature_dicts.tolist())

        # Combine the data
        self.df = pd.concat([self.df, feature_df, axis=1])
        self.df['vuln_category'] = self.df['vulnerability_type'].apply(self.categorize_vulnerability)

        print("Completed data preprocessing")
        return self.df
                                  
   
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

