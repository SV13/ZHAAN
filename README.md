# ZHAAN: Zero-trust Heuristic Automated Analysis for Navigation

### Project Overview
ZHAAN is a comprehensive, multi-layered command-line interface (CLI) security framework developed in Python. It is designed to address the limitations of traditional, static security systems by providing an end-to-end solution for detecting known and emerging cyber threats. The system combines various detection methods to analyze command-line inputs, URLs, and file hashes, offering a robust and adaptable defense mechanism.

### Key Features
* **Live Monitor Mode**: Actively monitors PowerShell command history and running processes in real-time. It applies both Rule-Based and Machine Learning analysis to provide instant threat alerts with timestamps.
* **Rule-Based Detection**: Uses a curated CSV dataset (`rules.csv`) to match commands against known malicious patterns. It provides detailed contextual information, including a description, threat score, and MITRE ATT&CK ID, for an explainable alert.
* **Machine Learning Detection**: Applies a trained SVM-based model to classify commands or URLs as Malicious, Suspicious, or Benign. The model provides a confidence score and highlights high-weight tokens to justify its predictions.
* **Malware File Hash Detection**: Scans a specified folder by computing the MD5, SHA1, and SHA256 hashes of all files and comparing them against a known malicious hash database (`mal.csv`).
* **Experimental ZHAAN GPT**: An experimental, NLP-based module that uses a fine-tuned T5 model to provide human-like reasoning. It provides a classification, a plain-language explanation of what a command or URL does, and a recommendation for next steps.
* **Log Management**: Offers a robust system for viewing, archiving, and exporting detection logs. It automatically rotates logs to manage file size and disk usage.

### System Architecture
ZHAAN operates as a cohesive framework where all detection methods are integrated and accessible via a central CLI.
* The **CLI interface** acts as the control center, allowing the user to trigger different functionalities.
* The **Live Monitor** serves as the primary real-time threat detection engine, correlating data from running processes and PowerShell history with the rule-based and machine learning models.
* The **detection backends** (`rule_engine.py`, `predictor.py`, `malware_scan.py`, and `t5_inference.py`) handle the core logic for their respective detection methods.
* The **Log Management** system (`log_manager.py`) transparently records all detection events for later review and auditing.

![ZHAAN Architecture](https://github.com/user-attachments/assets/97a7c560-1a4f-46bd-a780-0eb2fe3d98e0)



### Secure Coding Techniques
The project was developed with a focus on secure and reliable coding practices to ensure its stability and integrity.
* **Input Normalization**: All command inputs are cleaned and standardized (e.g., lowercasing, removing extra spaces) to prevent attackers from bypassing detection using formatting tricks.
* **Safe Defaults and Fallbacks**: The system is designed with secure baseline behaviors to prevent crashes from unexpected input or missing data.
* **Exception Handling**: `try-except` blocks are used to gracefully handle errors during system interactions, such as accessing processes or files, ensuring the program continues to run without crashing.
* **Controlled Use of Threading**: The Live Monitor uses separate threads for different tasks (e.g., monitoring processes, checking PowerShell history) to prevent resource conflicts and ensure responsiveness.
* **Minimal Use of Global State**: Global variables are used sparingly and only when necessary for thread synchronization, which helps keep the code modular and reduces the risk of data corruption.
* **Contextual Logging**: All detection events are logged with detailed information, including timestamps, sources, and detection results, to provide clear and traceable records for incident review and auditing.

### Installation & Dependencies
ZHAAN is a Python-based CLI tool. You can install it by cloning the repository and installing the required dependencies.

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/Sharveenn/ZHAAN.git](https://github.com/Sharveenn/ZHAAN.git)
    cd ZHAAN
    ```

2.  **Install Dependencies**:
    ZHAAN relies on several Python libraries. You can install all of them using `pip`:
    ```bash
    pip install colorama psutil pandas scikit-learn xgboost joblib transformers torch
    ```

3.  **Download Models & Datasets**:
    The system requires several local files to run:
    * `data/rules.csv`
    * `data/Z_ML_dataset.csv`
    * `data/mal.csv`
    * `models/zhaan_model.joblib`
    * `models/zhaan_vectorizer.joblib`
    * `models/zhaan_label_encoder.joblib`
    * `models/t5_zhaan/` (directory containing T5 model and tokenizer files)

    Make sure these files are present in their respective directories after cloning the repository. The models are not included in the main project but are trained using the provided scripts.

### Usage
To run the ZHAAN system, execute the main script:
```bash
python zhaan.py
```


