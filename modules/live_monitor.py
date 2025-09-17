import psutil
import time
import os
import threading
import hashlib
import re
from colorama import Fore, Style, init
from modules.predictor import predict_command
from modules.live_rule import load_rules, search_command
from modules.log_manager import log_event

init(autoreset=True)

SEEN_COMMANDS = set()
stop_monitoring = False

COLOR_MAP = {
    "Malicious": Fore.RED + "☠ Malicious",
    "Suspicious": Fore.YELLOW + "⚠ Suspicious",
    "Benign": Fore.GREEN + "✅ Benign"
}

POWERSHELL_HISTORY_PATH = os.path.expandvars(r"%APPDATA%\\Microsoft\\Windows\\PowerShell\\PSReadline\\ConsoleHost_history.txt")
CMD_HISTORY_TEMP_PATH = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "zhaan_cmd_history.log")

def advanced_validate_input(command):
    if not isinstance(command, str) or len(command.strip()) == 0:
        raise ValueError("Invalid command: input must be non-empty string.")
    # Detect control characters
    if any(ord(c) < 32 and c not in ('\t', '\n', '\r') for c in command):
        print(Fore.RED + "[!] Warning: Command contains potentially dangerous control characters.")
    return command

def normalize_command(command):
    command = command.lower().strip()
    command = re.sub(r"\s+", " ", command)  # collapse spaces
    command = command.replace("\\", "/")  # unify slashes for consistency
    return command

def display_result(process_name, cmdline, rule_result, ml_result):
    print(Fore.CYAN + "\n" + "─" * 50)
    print(f"{Fore.BLUE}[🔎] Source       : {process_name}")
    print(f"{Fore.BLUE}[🧠] Input        : {' '.join(cmdline)}")
    if rule_result and isinstance(rule_result, dict):
        print(f"\n{Fore.MAGENTA}[🎯] Rule-Based    : {COLOR_MAP.get(rule_result.get('type', 'Benign'), rule_result.get('type', 'Benign'))}")
        print(f"    Description : {rule_result.get('description', '-')}")
        print(f"    MITRE ID    : {rule_result.get('mitre_id', '-')} — {rule_result.get('technique', '-')}")
        print(f"    Score       : {rule_result.get('score', 0.0)}")
    if ml_result and isinstance(ml_result, dict):
        print(f"\n{Fore.CYAN}[🤖] ML Prediction: {COLOR_MAP.get(ml_result.get('label', 'Benign'), ml_result.get('label', 'Benign'))} ({ml_result.get('confidence', 0.0)}%)")
        print(f"    Why         : Tokens → {ml_result.get('top_tokens', [])}")
    print(Fore.CYAN + "─" * 50)

def input_listener():
    global stop_monitoring
    while True:
        key = input().strip().lower()
        if key == 'q':
            stop_monitoring = True
            break

def process_line(source, line, rules):
    if not line:
        return

    try:
        validated = advanced_validate_input(line)
    except ValueError:
        return

    normalized = normalize_command(validated)
    if normalized in SEEN_COMMANDS:
        return

    SEEN_COMMANDS.add(normalized)
    rule_match = search_command(rules, normalized) or {
        "type": "Benign",
        "description": "No rule match found.",
        "mitre_id": "-",
        "technique": "-",
        "score": 0.0
    }
    ml_match = predict_command(normalized)
    display_result(source, [line], rule_match, ml_match)
    log_event(f"[LIVE MONITOR] {source} | {line} | Rule: {rule_match.get('type')} ({rule_match.get('score')}) | ML: {ml_match.get('label')} ({ml_match.get('confidence')}%)")

def monitor_powershell_history(rules):
    last_hash = ""
    while not stop_monitoring:
        if os.path.exists(POWERSHELL_HISTORY_PATH):
            with open(POWERSHELL_HISTORY_PATH, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                if not lines:
                    continue
                current = lines[-1].strip()
                current_hash = hashlib.sha1(current.encode()).hexdigest()
                if current_hash != last_hash:
                    last_hash = current_hash
                    process_line("PowerShell", current, rules)
        time.sleep(2)

def monitor_processes(rules):
    while not stop_monitoring:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                name = proc.info['name']
                cmdline = proc.info['cmdline']
                if not cmdline:
                    continue
                full_cmd = ' '.join(cmdline)
                try:
                    validated = advanced_validate_input(full_cmd)
                except ValueError:
                    continue
                normalized = normalize_command(validated)
                if normalized in SEEN_COMMANDS:
                    continue
                SEEN_COMMANDS.add(normalized)
                rule_match = search_command(rules, normalized) or {
                    "type": "Benign",
                    "description": "No rule match found.",
                    "mitre_id": "-",
                    "technique": "-",
                    "score": 0.0
                }
                ml_match = predict_command(normalized)
                display_result(name, cmdline, rule_match, ml_match)
                log_event(f"[LIVE MONITOR] {name} | {full_cmd} | Rule: {rule_match.get('type')} ({rule_match.get('score')}) | ML: {ml_match.get('label')} ({ml_match.get('confidence')}%)")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        time.sleep(2)

def start_live_monitor():
    global stop_monitoring
    stop_monitoring = False

    print(Fore.GREEN + Style.BRIGHT + "\nZHAAN - Live Monitoring Started...")
    print(Fore.CYAN + "[Q] Press Q anytime to stop monitoring\n")

    rules = load_rules()
    listener = threading.Thread(target=input_listener, daemon=True)
    listener.start()

    powershell_thread = threading.Thread(target=monitor_powershell_history, args=(rules,), daemon=True)
    process_thread = threading.Thread(target=monitor_processes, args=(rules,), daemon=True)

    powershell_thread.start()
    process_thread.start()

    while not stop_monitoring:
        time.sleep(1)

    print(Fore.BLUE + "\n[!] Live Monitoring Stopped by User.")
    print(Fore.GREEN + Style.BRIGHT + "Returning to main menu...")
