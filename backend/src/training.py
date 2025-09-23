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
def prepare_ml_data(df):
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

# Train ML Models: Random Forest + Logistic Regression"
def train_models(df):
    X, y, vectorizer, encoder = prepare_ml_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    models = {
        'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'logistic_regression': LogisticRegression(max_iter=1000, random_state=42),
    }


    results = {}
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        print(f"{name} Accuracy {acc:.3f}")
        print(classification_report(y_test, preds, target_names=encoder_classes_))
        results[name] = model

    return results, vectorizer, encoder 

# Save the models and the preprocessing
def save_models(models, vectorizer, encoder, models_dir="models"):
    os.makedirs(models_dir, exist_ok=True)
    for name, model in models.items():
        with open(os.path.join(models_dir, f"{name}.pkl"), "wb") as f:
            pickle.dump(model, f)
    with open(os.path.join(models_dir, "vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)
    with open(os.path.join(models_dir, "label_encoder.pkl"), "wb") as f:
        pickle.dump(encoder, f)
    print("Models and preprocessors saved")