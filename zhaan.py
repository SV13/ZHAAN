from colorama import init, Fore, Style
import os
import sys
import time
import subprocess

# Initialize colorama
init(autoreset=True)

# Import modules
from modules.help_menu import show_help
from modules.rule_engine import rule_based_detection, set_logger
from modules import log_manager
from modules.predictor import predict_command, machine_learning_detection
from modules.live_monitor import start_live_monitor
from modules.t5_inference import run_t5_inference_cli
from modules.malware_scan import run_malware_scan

# Setup logging
log_manager.init_log_dir()
set_logger(log_manager.log_event)

# ASCII Banner
banner = f"""{Fore.BLUE}
 ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄ 
▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░▌      ▐░▌
 ▀▀▀▀▀▀▀▀▀█░▌▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌░▌     ▐░▌
          ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌▐░▌    ▐░▌
 ▄▄▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌ ▐░▌   ▐░▌
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌  ▐░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░▌   ▐░▌ ▐░▌
▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌    ▐░▌▐░▌
▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌     ▐░▐░▌
▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌       ▐░▌▐░▌      ▐░░▌
 ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀         ▀  ▀         ▀  ▀        ▀▀ 

     {Style.BRIGHT}{Fore.BLUE}Z.H.A.A.N. — Zero-trust Heuristic Automated Analysis for Navigation
                 Developed by Sharveenn Murthi{Style.RESET_ALL}
"""

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        print(Fore.CYAN + "-" * 45)
        print("[1] Live Monitor Mode")
        print("[2] Run Rule-Based Detection")
        print("[3] Run Machine Learning Detection")
        print("[4] Malware Identifier")
        print("[5] Experimental Zhaan GPT")
        print("[6] Log Management")
        print("[7] Help")
        print("[8] Exit")
        print("-" * 45)

        choice = input(Fore.YELLOW + "Select an option (1–8): ").strip()

        if choice == "1":
            start_live_monitor()
        elif choice == "2":
            rule_based_detection()
        elif choice == "3":
            machine_learning_detection()
        elif choice == "4":
            run_malware_scan()
        elif choice == "5":
            run_t5_inference_cli()
        elif choice == "6":
            log_manager.log_management_menu()
        elif choice == "7":
            show_help()
        elif choice == "8":
            print(Fore.BLUE + "\nExiting ZHAAN...")
            sys.exit()
        else:
            print(Fore.RED + "[!] Invalid input. Please enter a number between 1 and 8.")
            time.sleep(1.5)

if __name__ == "__main__":
    main_menu()
