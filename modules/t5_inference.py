import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import os

# Load model and tokenizer
model_path = os.path.join("models", "t5_zhaan")
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

# ANSI Colors
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


def predict_t5(input_text):
    input_ids = tokenizer.encode(input_text, return_tensors="pt", truncation=True)
    outputs = model.generate(input_ids, max_length=128, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def print_t5_banner():
    print(BLUE + r"""
 ______     __  __     ______     ______     __   __    
/\___  \   /\ \_\ \   /\  __ \   /\  __ \   /\ "-.\ \   
\/_/  /__  \ \  __ \  \ \  __ \  \ \  __ \  \ \ \-.  \  
  /\_____\  \ \_\ \_\  \ \_\ \_\  \ \_\ \_\  \ \_\\"\_\ 
  \/_____/   \/_/\/_/   \/_/\/_/   \/_/\/_/   \/_/ \/_/ 

 ______     ______   ______                             
/\  ___\   /\  == \ /\__  _\                            
\ \ \__ \  \ \  _-/ \/_/\ \/                            
 \ \_____\  \ \_\      \ \_\                            
  \/_____/   \/_/       \/_/                            
""" + RESET)
    print(f"{CYAN}ZHAAN GPT — T5-powered Reasoning Module{RESET}")
    print(f"{YELLOW}Type 'exit' to quit.{RESET}")
    print(f"{CYAN}Please start your query with the word 'Analyze' and the desired command, as the model do its best to give its reasoning.{RESET}\n")


def run_t5_inference_cli():
    print_t5_banner()
    while True:
        try:
            user_input = input(f"{CYAN}Enter the Command or URL to analyze: {RESET}").strip()
            if user_input.lower() == "exit":
                print(f"{YELLOW}Exiting ZHAAN GPT...{RESET}")
                break
            if not user_input.lower().startswith("analyze"):
                user_input = "Analyze: " + user_input

            result = predict_t5(user_input)

            print(f"\n{GREEN}🧠 Reasoning Result:{RESET}")
            print(f"{YELLOW}{result}{RESET}\n")

        except Exception as e:
            print(f"{RED}❌ Error: {str(e)}{RESET}")


# CLI entry point
if __name__ == "__main__":
    run_t5_inference_cli()
