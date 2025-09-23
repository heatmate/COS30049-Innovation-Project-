import os 
import pickle
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from scipy.sparse import hstack

# Prepare data or machine learning
def prepare_ml_data(self):
    # USING TF-IDF for text features 
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=2
    )

    text_features = vectorizer.fit_transform(df['clean_code'])
    feature_cols = ['has_user_input', 'has_db_operation', 'has_file_operation', 'has_eval', 
                    'code_length', 'has_validation', 'has_quotes','has_concatenation']
    numerical = df[feature_cols].astype(int)

# Combine features 
    X = hstack([text_features, numerical.values])     
    encoder = LabelEncoder()
    y = encoder.fit_transform(df['vuln_category'])   

    return X, y, vectorizer, encoder

# Train MULTIPLE ML models
def train_models