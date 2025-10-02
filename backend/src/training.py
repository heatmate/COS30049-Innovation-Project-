import os 
import pickle
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, mean_squared_error, r2_score
from scipy.sparse import hstack
from sklearn.ensemble import RandomForestRegressor

# Prepare ML dataset and targets for the models
def prepare_ml_data(df, target_class='vuln_category', target_reg='vul'):
    # USING TF-IDF for text features 
    vectorizer = TfidfVectorizer(
        max_features=500,
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
    y_class = encoder.fit_transform(df[target_class])
    y_reg = df[target_reg].astype(float).values
     
    return X, y_class, y_reg, vectorizer, encoder

# Train ML Models: Random Forest + Logistic Regression" CHANGED TO EACH MODEL
def train_models(df):
    X, y_class, y_reg, vectorizer, encoder = prepare_ml_data(df)
    X_train, X_test, y_train_class, y_test_class, y_train_reg, y_test_reg = train_test_split(
    X, y_class, y_reg, test_size=0.2, stratify=y_class, random_state=42
)
    log_model = LogisticRegression(max_iter=1000, random_state=42)
    rf_model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=1)

    print("Training Logistic Regression (classification)...")
    log_model.fit(X_train, y_train_class)
    y_pred_class = log_model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test_class, y_pred_class):.3f}")
    print(classification_report(y_test_class, y_pred_class, target_names=encoder.classes_))

    print("\nTraining Random Forest (regression)...")
    rf_model.fit(X_train, y_train_reg)
    y_pred_reg = rf_model.predict(X_test)
    print(f"MSE: {mean_squared_error(y_test_reg, y_pred_reg):.3f}")
    print(f"R2 Score: {r2_score(y_test_reg, y_pred_reg):.3f}")

    return {'logistic_regression': log_model, 'random_forest_regressor': rf_model}, vectorizer, encoder

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