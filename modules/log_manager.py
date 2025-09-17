import os
import time
import shutil
from colorama import Fore, Style

log_dir = "logs"
log_file = os.path.join(log_dir, "zhaan_log.txt")
max_log_size_file = os.path.join(log_dir, "max_log_size.txt")
default_max_size = 500 * 1024  # 500 KB


def init_log_dir():
    """Ensure the log directory and size file exist"""
    os.makedirs(log_dir, exist_ok=True)
    if not os.path.exists(max_log_size_file):
        with open(max_log_size_file, "w") as f:
            f.write(str(default_max_size))


def get_max_log_size():
    """Read max log size from file"""
    try:
        with open(max_log_size_file, "r") as f:
            return int(f.read().strip())
    except:
        return default_max_size


def set_max_log_size():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + "\nZHAAN - Set Max Log File Size")
    print("-" * 40)
    print("Enter the new max size in KB (e.g., 250, 1024):")

    size_input = input("New size (KB): ").strip()
    if not size_input.isdigit():
        print(Fore.RED + "[!] Invalid size entered.")
        input("Press [Enter] to return...")
        return

    new_size = int(size_input) * 1024
    with open(max_log_size_file, "w") as f:
        f.write(str(new_size))
    print(Fore.GREEN + f"[✓] Log file size limit set to {size_input} KB.")
    input("Press [Enter] to return...")


def rotate_logs():
    """Rotate if active log exceeds max size"""
    max_size = get_max_log_size()
    if os.path.exists(log_file) and os.path.getsize(log_file) >= max_size:
        i = 1
        while os.path.exists(os.path.join(log_dir, f"zhaan_log_{i}.txt")):
            i += 1
        rotated_name = os.path.join(log_dir, f"zhaan_log_{i}.txt")
        os.rename(log_file, rotated_name)
        print(Fore.BLUE + f"[i] Log rotated: {rotated_name}")


def log_event(event):
    try:
        rotate_logs()
        with open(log_file, "a", encoding="utf-8") as f:
            timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
            f.write(f"{timestamp} {event}\n")
    except Exception as e:
        print(Fore.RED + f"[!] Logging error: {e}")


def view_current_log():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.YELLOW + Style.BRIGHT + "\nZHAAN - Active Log File")
    print("-" * 50)

    if not os.path.exists(log_file):
        print("[!] Active log file not found.")
    else:
        with open(log_file, "r", encoding="utf-8") as f:
            logs = f.read()
            print(logs if logs else "[*] Log is empty.")

    print("-" * 50)
    input("Press [Enter] to return...")


def list_logs():
    print(Fore.YELLOW + "\nAvailable Log Files:")
    print("-" * 40)
    logs = [f for f in os.listdir(log_dir) if f.startswith("zhaan_log")]
    if logs:
        for log_name in sorted(logs):
            full_path = os.path.join(log_dir, log_name)
            size_kb = os.path.getsize(full_path) // 1024
            print(f"{log_name} ({size_kb} KB)")
    else:
        print("No logs found.")
    print("-" * 40)
    input("Press [Enter] to return...")


def export_logs():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + Style.BRIGHT + "\nZHAAN - Export Log")
    print("-" * 50)

    logs = [f for f in os.listdir(log_dir) if f.startswith("zhaan_log")]
    if not logs:
        print(Fore.RED + "[!] No logs available to export.")
        input("Press [Enter] to return...")
        return

    print("Available Logs:")
    for i, log_name in enumerate(sorted(logs), 1):
        print(f"[{i}] {log_name}")

    choice = input("Select log to export by number: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(logs)):
        print(Fore.RED + "[!] Invalid selection.")
        input("Press [Enter] to return...")
        return

    selected_log = logs[int(choice) - 1]
    source_path = os.path.join(log_dir, selected_log)

    target_path = input("\nEnter export path (e.g. D:\\Backup\\log.txt): ").strip()
    try:
        shutil.copy(source_path, target_path)
        print(Fore.GREEN + f"[✓] Exported {selected_log} to {target_path}")
    except Exception as e:
        print(Fore.RED + f"[!] Export failed: {e}")

    input("Press [Enter] to return...")


def log_management_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        logs_count = len([f for f in os.listdir(log_dir) if f.startswith("zhaan_log")])
        max_size_kb = get_max_log_size() // 1024

        print(Fore.MAGENTA + Style.BRIGHT + "ZHAAN - Log Management")
        print("-" * 45)
        print(f"Current log files  : {logs_count}")
        print(f"Max size per log   : {max_size_kb} KB")
        print("-" * 45)
        print("[1] View Current Log")
        print("[2] View All Logs")
        print("[3] Export Log File")
        print("[4] Set Max Log File Size")
        print("[5] Return to Main Menu")
        print("-" * 45)

        choice = input("Select an option (1–5): ").strip()
        if choice == "1":
            view_current_log()
        elif choice == "2":
            list_logs()
        elif choice == "3":
            export_logs()
        elif choice == "4":
            set_max_log_size()
        elif choice == "5":
            break
        else:
            print(Fore.RED + "[!] Invalid choice.")
            time.sleep(1.5)
