import numpy as np
from scipy.sparse import hstack
from .features import clean_code, extract_features

# Predict Vulnerability for a code snippet
def predict_vulnerability(code_snippet, model, vectorizer, encoder):
    """Predict vulnerability for a code snippet"""
    clean = clean_code(code_snippet)
    features = extract_features(code_snippet)

    text = vectorizer.transform([clean])
    feature_cols = ['has_user_input','has_db_operation','has_file_operation',
                    'has_eval','code_length','has_validation','has_quotes','has_concatenation']
    numerical = np.array([[features.get(c, 0) for c in feature_cols]])

    X = hstack([text, numerical])
    pred = model.predict(X)[0]
    probs = model.predict_proba(X)[0]
    return {
        "vulnerability_category": encoder.inverse_transform([pred])[0],
        "confidence": max(probs),
        "probabilities": dict(zip(encoder.classes_, probs))
    }
