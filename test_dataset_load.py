import csv
import os
from collections import Counter

def test_minimal_dataset():
    dataset_path = os.path.join("data", "Z_ML_dataset.csv")

    try:
        with open(dataset_path, mode='r', encoding='latin-1') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            if not rows:
                print("Dataset is empty.")
                return

            print(f"Dataset loaded successfully with {len(rows)} entries.\n")

            # Show column headers
            print("🧾 Column Headers:")
            print("  " + ", ".join(reader.fieldnames))
            print("\n📄 Sample Entry:")
            sample = rows[0]
            for key, value in sample.items():
                print(f"  {key}: {value}")

            # Count by label
            label_counts = Counter(row["Label"].strip().lower() for row in rows)
            print("\n📊 Entry Counts by Label:")
            for label, count in label_counts.items():
                emoji = {
                    "malicious": "🛑",
                    "suspicious": "⚠️",
                    "benign": "✅"
                }.get(label, "❓")
                print(f"  {emoji} {label.capitalize()}: {count}")

    except FileNotFoundError:
        print("[❌] File not found. Please make sure 'Z_ML_dataset.csv' is in the 'data/' folder.")
    except UnicodeDecodeError:
        print("[❌] UnicodeDecodeError: File may not be saved in Latin-1 encoding.")
    except KeyError:
        print("[❌] Expected 'Prompt' and 'Label' columns not found.")
    except Exception as e:
        print(f"[❌] Unexpected error: {e}")

if __name__ == "__main__":
    test_minimal_dataset()
