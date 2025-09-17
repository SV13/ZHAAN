import os
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# Define paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "Z_ML_dataset.csv")
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "zhaan_model.joblib")
VECTORIZER_PATH = os.path.join(PROJECT_ROOT, "models", "zhaan_vectorizer.joblib")

# Confirm path to dataset
print(f"[📂] Loading dataset from: {DATA_PATH}")

# Load dataset
try:
    df = pd.read_csv(DATA_PATH, encoding="latin-1")
    print(f"Dataset loaded successfully with {len(df)} entries.")
    print(f"Dataset Columns: {list(df.columns)}\n")
except Exception as e:
    print(f"Failed to load dataset: {e}")
    exit(1)

# Show sample
print("Sample Row:")
print(df.head(1).to_string(index=False), "\n")

# Load model and vectorizer
try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("Model and vectorizer loaded.\n")
except Exception as e:
    print(f"Failed to load model/vectorizer: {e}")
    exit(1)

# Preprocess text data
def preprocess_input(command):
    command = command.lower()
    command = re.sub(r'[\W_]+', ' ', command)
    return command.strip()

df['Processed'] = df['Prompt'].astype(str).apply(lambda x: x.lower())

# Vectorize
X = vectorizer.transform(df['Processed'])
y_true = df['Label']

# Predict
y_pred = model.predict(X)

# Accuracy
accuracy = accuracy_score(y_true, y_pred)
print("Model Evaluation Report")
print("-" * 40)
print(f"Accuracy: {accuracy:.2f}\n")
print("Classification Report:")
print(classification_report(y_true, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_true, y_pred, labels=["Malicious", "Suspicious", "Benign"])
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap="Blues", xticklabels=["Malicious", "Suspicious", "Benign"], yticklabels=["Malicious", "Suspicious", "Benign"])
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()
