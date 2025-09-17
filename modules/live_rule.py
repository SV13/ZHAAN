import csv
import os
import re
from colorama import Fore

# Path to rule-based dataset
RULES_PATH = os.path.join("data", "rules.csv")
logger = None

def set_logger(log_func):
    global logger
    logger = log_func

def load_rules(filepath="rules.csv"):
    """Load CSV file into memory"""
    if not os.path.exists(filepath):
        print(Fore.RED + f"[!] Dataset file '{filepath}' not found.")
        return []

    with open(filepath, "r", encoding="latin-1") as f:
        reader = csv.DictReader(f)
        return list(reader)

def normalize_input(command):
    command = command.lower().strip()
    command = re.sub(r"\\s+", " ", command)
    command = command.replace("\\", "/")
    return command

def search_command(rules, user_input):
    normalized_input = normalize_input(user_input)
    for row in rules:
        rule_prompt = normalize_input(row["Prompt"])
        if rule_prompt == normalized_input:
            return {
                "type": row.get("Type", "Benign"),
                "description": row.get("Description", "-"),
                "mitre_id": row.get("MITRE ID", "-"),
                "technique": row.get("MITRE Technique", "-"),
                "score": float(row.get("Score", 0.0))
            }
    return None

def rule_based_detection():
    rules = load_rules()
    if not rules:
        return

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + "ZHAAN - Rule-Based Detection")
        print("-" * 40)
        user_input = input("Enter a command to analyze: ").strip()

        match = search_command(rules, user_input)
        if match:
            type_label = match['type']
            color = Fore.GREEN if type_label == "Benign" else Fore.YELLOW if type_label == "Suspicious" else Fore.RED
            print(color + f"\n[!] Classification: {type_label}")
            print(Fore.CYAN + f"    Description : {match['description']}")
            print(Fore.CYAN + f"    MITRE ID    : {match['mitre_id']} — {match['technique']}")
            print(Fore.CYAN + f"    Score       : {match['score']}")
        else:
            print(Fore.YELLOW + "\n[!] No rule found for this command. Classified as Unknown.")

        if logger:
            logger(f"[RULE] {user_input} → {match['type'] if match else 'Unknown!] Match Found in Live Rule Scan'}")

        print("\n[1] Try another command")
        print("[2] Return to Main Menu")
        choice = input("Select an option: ").strip()
        if choice != "1":
            break
