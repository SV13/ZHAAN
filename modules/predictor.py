import os
import joblib
import re
import numpy as np
from sklearn.linear_model import LogisticRegression
from colorama import Fore
from modules import log_manager

# Set secure project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "zhaan_model.joblib")
VECTORIZER_PATH = os.path.join(PROJECT_ROOT, "models", "zhaan_vectorizer.joblib")

# Load model and vectorizer
try:
    model: LogisticRegression = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
except Exception as e:
    print(f"[❌] Failed to load model/vectorizer: {e}")
    log_manager.log_event(f"[ERROR] Failed to load ML model/vectorizer: {e}")
    model = None
    vectorizer = None

def advanced_validate_input(command):
    """Ensure command is a safe, valid input"""
    if not isinstance(command, str) or len(command.strip()) == 0:
        raise ValueError("Input must be a non-empty string.")
    if any(ord(c) < 32 and c not in ('\t', '\n', '\r') for c in command):
        print(Fore.RED + "[!] Warning: Control characters detected in input.")
    return command

def preprocess_input(command):
    command = command.lower()
    command = re.sub(r'[\W_]+', ' ', command)
    return command.strip()

def explain_top_tokens(command, vectorizer, top_n=5):
    tfidf_matrix = vectorizer.transform([command])
    tokens = vectorizer.get_feature_names_out()
    weights = tfidf_matrix.toarray()[0]

    top_indices = weights.argsort()[::-1][:top_n]
    top_tokens = [tokens[i] for i in top_indices if weights[i] > 0]
    return top_tokens

def predict_command(user_input):
    if not model or not vectorizer:
        return "[❌] Model or vectorizer not available."

    processed = preprocess_input(user_input)
    vectorized = vectorizer.transform([processed])

    prediction = model.predict(vectorized)[0]
    confidence = np.max(model.predict_proba(vectorized)) * 100
    top_tokens = explain_top_tokens(processed, vectorizer)

    return {
        "label": prediction,
        "confidence": round(confidence, 2),
        "top_tokens": top_tokens
    }

def machine_learning_detection():
    """Interactive CLI for ML-based detection"""
    while True:
        print("\nZHAAN - Machine Learning Detection")
        print("----------------------------------------")
        command = input("Enter a command to analyze: ")

        try:
            validated = advanced_validate_input(command)
        except ValueError as ve:
            print(Fore.RED + f"[!] {ve}")
            log_manager.log_event(f"ML Detection Error | Invalid Input: {command}")
            input("Press [Enter] to try again...")
            continue

        result = predict_command(validated)

        if isinstance(result, dict):
            label = result['label']
            confidence = result['confidence']
            tokens = result['top_tokens']

            color = (
                Fore.RED if label.lower() == 'malicious'
                else Fore.YELLOW if label.lower() == 'suspicious'
                else Fore.GREEN
            )
            print(f"\nPrediction: {color}{label} ({confidence}%)")
            print(f"Why: High-weight tokens detected: {tokens}\n")

            log_manager.log_event(
                f"ML Detection | Prompt: '{command}' | Result: {label} ({confidence}%) | Tokens: {tokens}"
            )
        else:
            print(result)
            log_manager.log_event(f"ML Detection Error | Prompt: '{command}' | Error: {result}")

        print("1. Try another command")
        print("2. Return to main menu")
        follow_up = input("Select an option (1–2): ").strip()
        if follow_up == "2":
            break
