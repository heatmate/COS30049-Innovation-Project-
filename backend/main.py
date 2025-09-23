from src.processor import VulnerabilityDataProcessor
from src.training import train_models, save_models

if __name__ == "__main__":
    processor = VulnerabilityDataProcessor()
    
    # Load data
    df, error_df = processor.load_data()  # <-- now returns both valid & invalid
    
    if df.empty:
        print("No valid rows found. Proceeding to analyze invalid/malformed code...")
        print(error_df.head())
    else:
        # Preprocess valid data only
        df = processor.preprocess_data()
        
        # Train
        models, vectorizer, encoder = train_models(df)
        save_models(models, vectorizer, encoder)
        
        # Test prediction
        test_code = """
        const query = `SELECT * FROM users WHERE id = ${userId}`;
        db.query(query, (err, results) => {
            res.json(results);
        });
        """
        prediction = predict_vulnerability(test_code, models['random_forest'], vectorizer, encoder)
        print("Prediction:", prediction)
