import os
import csv
import re
import joblib
import hashlib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score

# Base path setup for project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(PROJECT_ROOT, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "zhaan_model.joblib")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "zhaan_vectorizer.joblib")
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "Z_ML_dataset.csv")

# Ensure model directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

def load_data():
    try:
        df = pd.read_csv(DATA_PATH, encoding='latin-1')
        df = df[['Prompt', 'Label']].dropna()
        return df
    except Exception as e:
        print(f"[❌] Failed to load dataset: {e}")
        return pd.DataFrame()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[\W_]+', ' ', text)  # Remove special characters
    return text.strip()

def train_model():
    df = load_data()
    if df.empty:
        return

    df['clean'] = df['Prompt'].apply(preprocess_text)
    X = df['clean']
    y = df['Label']

    # Vectorize
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1000)
    X_vec = vectorizer.fit_transform(X)

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, stratify=y, random_state=42)

    # Train models
    print("Training Logistic Regression...")
    lr_model = LogisticRegression(max_iter=500)
    lr_model.fit(X_train, y_train)

    print("Training Naive Bayes...")
    nb_model = MultinomialNB()
    nb_model.fit(X_train, y_train)

    # Evaluate both
    print("\nLogistic Regression Report:")
    y_pred_lr = lr_model.predict(X_test)
    print(classification_report(y_test, y_pred_lr))

    print("\nNaive Bayes Report:")
    y_pred_nb = nb_model.predict(X_test)
    print(classification_report(y_test, y_pred_nb))

    # Save best model (Logistic Regression)
    joblib.dump(lr_model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"Model and vectorizer saved to '{MODEL_DIR}'")

    # Secure hash output
    with open(MODEL_PATH, 'rb') as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()
        print(f"Model SHA256: {sha256}")

if __name__ == "__main__":
    train_model()
