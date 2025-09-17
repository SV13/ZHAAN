import csv
import os
import re
from colorama import Fore, Style

# Reference: zhaan_log.txt is written by zhaan.py
log_function = None  # to be set by zhaan.py

def set_logger(logger):
    global log_function
    log_function = logger

def advanced_validate_input(command):
    """Ensure command is a safe, valid input"""
    if not isinstance(command, str) or len(command.strip()) == 0:
        raise ValueError("Input must be a non-empty string.")
    if any(ord(c) < 32 and c not in ('\t', '\n', '\r') for c in command):
        print(Fore.RED + "[!] Warning: Control characters detected in input.")
    return command

def load_rules(filepath="rules.csv"):
    """Load CSV file into memory"""
    if not os.path.exists(filepath):
        print(Fore.RED + f"[!] Dataset file '{filepath}' not found.")
        return []

    with open(filepath, "r", encoding="latin-1") as f:
        reader = csv.DictReader(f)
        return list(reader)

def search_command(rules, user_input):
    """Search for exact match in Prompt column (case-insensitive)"""
    for row in rules:
        if row["Prompt"].strip().lower() == user_input.strip().lower():
            return row
    return None

def print_result(row):
    """Prints the results with proper formatting and color"""
    print(Style.BRIGHT + Fore.CYAN + "\n--- Command Match Found ---")
    print(Fore.WHITE + f"Prompt       : {row['Prompt']}")
    print(f"Description  : {row['Description']}")
    print(f"LOLBin       : {row['LOLBin']}")
    print(f"Content      : {row['Content']}")
    print(f"Frequency    : {row['Frequency']}")
    print(f"Source       : {row['Source']}")
    print(f"Network      : {row['Network']}")
    print(f"Behavioural  : {row['Behavioural']}")
    print(f"History      : {row['History']}")
    print(f"MITRE ID     : {row['MITRE ID']}")
    print(f"Technique    : {row['MITRE Technique']}")
    print(f"Score        : {row['Score']}")

    risk_type = row['Type'].strip().lower()
    if risk_type == "malicious":
        risk_color = Fore.RED
    elif risk_type == "suspicious":
        risk_color = Fore.YELLOW
    else:
        risk_color = Fore.GREEN

    print(risk_color + Style.BRIGHT + f"Classification: {row['Type'].upper()}")
    print(Fore.CYAN + "-" * 40)

def rule_based_detection():
    """Main rule-based detection loop"""
    rules = load_rules()
    if not rules:
        input("Press [Enter] to return to main menu...")
        return

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.MAGENTA + Style.BRIGHT + "ZHAAN - Rule-Based Detection")
        print("-" * 40)
        user_input = input(Fore.CYAN + "Enter a command to analyze: ").strip()

        try:
            validated = advanced_validate_input(user_input)
        except ValueError as ve:
            print(Fore.RED + f"[!] {ve}")
            input("Press [Enter] to try again...")
            continue

        match = search_command(rules, validated)

        if match:
            print_result(match)
            if log_function:
                log_function(f"Rule-Based | {match['Prompt']} | Score: {match['Score']} | Type: {match['Type']}")
        else:
            print(Fore.CYAN + "\n[!] Command not found in dataset.")
            if log_function:
                log_function(f"Rule-Based | {validated} | Not Found in Dataset")

        print("\nWhat would you like to do?")
        print("[1] Try another command")
        print("[2] Return to main menu")
        choice = input("Select an option (1 or 2): ").strip()

        if choice == "2":
            break
