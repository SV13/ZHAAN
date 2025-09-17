
# modules/t5_train.py

from transformers import T5Tokenizer, T5ForConditionalGeneration, Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
from datasets import Dataset
import pandas as pd
import os
import time

# === Paths ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "ZHAAN_T5_Training_Cleaned.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models", "t5_zhaan")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# === Load Dataset ===
df = pd.read_csv(DATA_PATH)
df.dropna(subset=["input_text", "target_text"], inplace=True)
dataset = Dataset.from_pandas(df)

# === Tokenizer & Model ===nnnn
model_name = "t5-base"  # or "t5-small" for faster training
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# === Preprocessing ===
def preprocess(example):
    input_enc = tokenizer(example["input_text"], truncation=True, padding="max_length", max_length=256)
    target_enc = tokenizer(example["target_text"], truncation=True, padding="max_length", max_length=256)
    input_enc["labels"] = target_enc["input_ids"]
    return input_enc

tokenized_dataset = dataset.map(preprocess, batched=True)
split = tokenized_dataset.train_test_split(test_size=0.1)

# === Training Arguments ===
training_args = Seq2SeqTrainingArguments(
    output_dir=MODEL_DIR,
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    weight_decay=0.01,
    save_total_limit=2,
    num_train_epochs=4,
    predict_with_generate=True,
    logging_dir=LOG_DIR,
    logging_steps=50,
    save_strategy="epoch",
    report_to="none",        # disables TensorBoard/W&B
    disable_tqdm=False       # enable progress bar
)

# === Trainer Setup ===
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=split["train"],
    eval_dataset=split["test"],
    tokenizer=tokenizer,
    data_collator=DataCollatorForSeq2Seq(tokenizer, model),
)

# === Train ===
if __name__ == "__main__":
    print("Starting T5 training...")
    start = time.time()
    trainer.train()
    end = time.time()
    print(f"Training completed in {(end - start)/60:.2f} minutes")
    trainer.save_model(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)
