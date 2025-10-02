import os 
import pandas as pd
from src.processor_json import VulnerabilityDataProcessor
from src.processor_csv import CSVProcessor
from src.training import train_models, save_models

def main():
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)

    # JSON Dataset (Given Sample)
    print("Processing JSON Dataset")
    json_process = VulnerabilityDataProcessor(data_path="data/raw/basic_data_3.jsonl")
    df_json, errors = json_process.load_data()
    df_json = json_process.preprocess_data()
    df_json.to_csv(os.path.join(processed_dir, "json.processed.csv"), index=False)

    # The CSV Dataset (Relevent Dataset Choice)
    print("Processing CSV Dataset")
    csv_process = CSVProcessor(
        csv_path="data/raw/vulnerability_fix_dataset.csv",
        output_path=os.path.join(processed_dir, "csv_processes.csv")
    )
    df_csv = csv_process.run()

    # Combining the two datasets
    print("Combining the 2 datasets")
    combined = pd.concat([df_json, df_csv], ignore_index=True)
    combined.to_csv(os.path.join(processed_dir, "combined_dataset.csv"), index=False)
    print(f"Final Dataset Shape: {combined.shape}")

    print("NaNs in regression target:", combined['vul'].isna().sum())

    # ML Model Training
    print("Training Models.........")
    models, vectorizer, encoder = train_models(combined)
    save_models(models, vectorizer, encoder, models_dir="models")

if __name__ == "__main__":
    main()