import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# heres how we config
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "combined_dataset.csv")
PLOTS_DIR = os.path.join(BASE_DIR, "plots")

os.makedirs(PLOTS_DIR, exist_ok=True)

print("Loading processed dataset...")
df = pd.read_csv(DATA_PATH, low_memory=False)
print(f"Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns\n")

#Identify the label column automatically 
label_col = None
for possible in ["vul", "vuln_category", "target"]:
    if possible in df.columns:
        label_col = possible
        break

if label_col is None:
    raise ValueError("Could not find a label column (expected 'vul' or 'vuln_category').")

print(f"Using '{label_col}' as target column.\n")

# === Correlation Heatmap ===
numeric_df = df.select_dtypes(include=["number", "bool"]).copy()
if label_col in numeric_df.columns:
    corr = numeric_df.corr(numeric_only=True)
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, cmap="coolwarm", annot=False)
    plt.title("Correlation Heatmap of Numerical Features")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "correlation_heatmap.png"))
    plt.show()
else:
    print("(no numeric target found).")

# === Distribution of Label Column ===
plt.figure(figsize=(8, 6))
if df[label_col].dtype == "object":
    df[label_col].value_counts().plot(kind="bar", color="skyblue")
    plt.title(f"Distribution of {label_col} Categories")
else:
    sns.histplot(df[label_col], kde=True, color="orange")
    plt.title(f"Distribution of {label_col} Values")

plt.xlabel(label_col)
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, f"{label_col}_distribution.png"))
plt.show()

# Compare model metrics
metrics_path = os.path.join(BASE_DIR, "models", "model_metrics.csv")
if os.path.exists(metrics_path):
    metrics_df = pd.read_csv(metrics_path)
    plt.figure(figsize=(8, 6))
    sns.barplot(x="Model", y="Score", data=metrics_df)
    plt.title("Model Performance Comparison")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "model_comparison.png"))
    plt.show()
else:
    print("ℹNo model metrics found.")

print(f"\nAll visualizations saved : {PLOTS_DIR}")
