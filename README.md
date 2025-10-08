How to Run
Create and activate the virtual environment
GO - cd software-detection 
then - cd backend
then - python -m venv venv
venv\Scripts\activate     # Windows
or 
source venv/bin/activate  # Mac

INSTALL DEPENDENDS
pip install -r requirements.txt

Run the main training pipeline
cd backend
python main.py

this command does this:
Loads and cleans the datasets
Combines JSON + CSV data
Trains both classification and regression models
Saves results in backend/models/

Generate visualizations!!!!
cd src
python visualization.py

This produces - 
correlation_heatmap.png
vulnerability_distribution.png

All saved i -
backend/plots/

Model Results
Logistic Regression	Classification	Accuracy	0.947
Random Forest	Regression	R² Score	0.985

Visualizations:
Correlation Heatmap — shows relationships between numerical features
Label Distribution Chart — displays vulnerability type frequencies

(Optional) Model Comparison Chart

Notes:
2 Datasets Used found on Kaggle and Initial assignment

Author

Heath Sullivan, Jean Palamara, Matthew Docherty 
COS30049 — Software Innovation Project
Swinburne University of Technology — 2025
