
import os
import re
import joblib
import hashlib
import pandas as pd
import numpy as np
import time
from tqdm import tqdm
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import VotingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

# ==== Paths ====
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "Z_ML_dataset.csv")
MODEL_DIR = os.path.join(PROJECT_ROOT, "models", "final_ml")
os.makedirs(MODEL_DIR, exist_ok=True)

# ==== Load and preprocess data ====
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
    text = re.sub(r'[\W_]+', ' ', text)
    return text.strip()

# ==== Train model ====
def train_model():
    print("[📥] Loading dataset...")
    df = load_data()
    if df.empty:
        return

    df['clean'] = df['Prompt'].apply(preprocess_text)

    X = df['clean']
    y = df['Label']

    print("[🔠] Vectorizing with TF-IDF...")
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=2000)
    X_vec = vectorizer.fit_transform(X)

    print("[🔃] Encoding labels...")
    label_encoder = LabelEncoder()
    y_enc = label_encoder.fit_transform(y)

    print("[✂️] Splitting train/test...")
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y_enc, test_size=0.2, stratify=y_enc, random_state=42)

    print("[⚙️] Initializing models...")
    svc = CalibratedClassifierCV(LinearSVC())
    xgb = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')

    voting_model = VotingClassifier(
        estimators=[
            ('svc', svc),
            ('xgb', xgb)
        ],
        voting='soft'
    )

    print("[🚀] Training VotingClassifier...")
    start_time = time.time()
    for _ in tqdm(range(1), desc="Training Progress"):
        voting_model.fit(X_train, y_train)
    end_time = time.time()

    print("[🧪] Evaluating model...")
    y_pred = voting_model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"[✅] Accuracy: {acc:.4f}")

    print("[💾] Saving model artifacts...")
    joblib.dump(voting_model, os.path.join(MODEL_DIR, "zhaan_model.joblib"))
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, "zhaan_vectorizer.joblib"))
    joblib.dump(label_encoder, os.path.join(MODEL_DIR, "zhaan_label_encoder.joblib"))

    with open(os.path.join(MODEL_DIR, "zhaan_model.joblib"), 'rb') as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()
        print(f"[🔐] Model SHA256: {sha256}")

    print(f"[⏱️] Training duration: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    train_model()
