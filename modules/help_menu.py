from colorama import Fore, Style
import os

def show_help():
    """Display the updated Help Menu."""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + Style.BRIGHT + "\nZHAAN - Help Menu")
        print("-" * 50)
        print("ZHAAN (Zero-day Heuristic & Analysis for Anomalous Navigation)")
        print("A CLI-based security tool for detecting threats from commands, URLs, and file hashes.\n")

        print("[1] Live Monitor (Real-Time Detection):")
        print("    - Actively monitors PowerShell history.")
        print("    - Applies both Rule-Based and Machine Learning analysis.")
        print("    - Logs every detection with timestamps.\n")

        print("[2] Rule-Based Inspection:")
        print("    - Uses a weighted scoring system from a curated CSV dataset.")
        print("    - Labels commands as Malicious, Suspicious, or Benign.")
        print("    - Provides reasoning and context behind each label.\n")

        print("[3] Machine Learning Detection:")
        print("    - Applies an SVM-based model to classify commands or URLs.")
        print("    - Highlights high-weight tokens and outputs a confidence score.\n")

        print("[4] Malware File Hash Detection:")
        print("    - Scans a folder’s files for known malware signatures.")
        print("    - Compares file hashes against a known malicious hash database.\n")

        print("[5] ZHAAN GPT - T5 Reasoning:")
        print("    - NLP-based model that provides classification, explanation, and recommendation.")
        print("    - Accepts human-like input prefixed with 'analyze:' for advanced analysis.\n")

        print("[6] Log Management:")
        print("    - Option 1: View active log content.")
        print("    - Option 2: View available log files.")
        print("    - Option 3: Export a log file to a custom path.")
        print("    - Option 4: Set maximum log file size (in KB).\n")

        print("[7] Help:")
        print("    - Displays this help screen.\n")

        print("[8] Exit:")
        print("    - Cleanly exits ZHAAN.\n")

        print("Note: ZHAAN never executes input commands. All inputs are sanitized and securely logged.")
        print("-" * 50)
        input("Press [Enter] to return to main menu...")
        break
