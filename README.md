ThreatGuard-AI Security Agent — Kaggle Version

A modular, AI-powered security scanner that runs fully inside Kaggle notebooks — no local environment needed.

🚀 Project Overview

ThreatGuard-AI is a lightweight security agent built to:

Scan files

Analyze system-like parameters

Detect risks

Return alerts with risk scores

Provide automated recommended actions

This version is optimized to run directly inside Kaggle, allowing judges to reproduce your results instantly.
<img width="1714" height="1514" alt="download" src="https://github.com/user-attachments/assets/b6e0b3e1-185d-4d68-a8a7-f5e0aa2e6fd8" />

📦 Repository Structure
ThreatGuard-AI-Security-Agent/
│
├── README.md                # Project overview
│
├── api/                     # FastAPI backend
│   ├── server.py            # Main server file
│   └── routes/              # All API routes live here
│       ├── action.py
│       ├── file_scan.py
│       └── system_scan.py
│
├── config/
│   └── settings.yaml        # All config values (paths, flags, etc.)
│
├── logs/                    # Runtime logs (created automatically)
│
├── src/                     # Core AI agent code
│   ├── main.py              # Entry point for running the agent
│   │
│   ├── agents/              # Different AI agents
│   │   ├── action_agent.py
│   │   ├── gemini_agent.py
│   │   ├── orchestrator_agent.py
│   │   └── threat_detection_agent.py
│   │
│   ├── memory/              # AI memory system
│   │   ├── memory_agent.py
│   │   └── memory_bank.py
│   │
│   ├── tools/               # Security tools used by the agents
│   │   ├── file_scanner.py
│   │   ├── filescan.py
│   │   ├── system_analyzer.py
│   │   └── system_hardener.py
│   │
│   └── utils/
│       └── logger.py        # Simple logger wrapper
-


🧪 Running the Project on Kaggle

Judges do NOT need to set up virtual environments or install packages manually.
Everything runs inside the Kaggle notebook using these exact steps:

✔ 1. Load Kaggle Secrets (Optional)

 Configure your Gemini API Key
This notebook uses the Gemini API, which requires an API key.

1. Get your API key

If you don't have one already, create an API key in Google AI Studio.

2. Add the key to Kaggle Secrets

Next, you will need to add your API key to your Kaggle Notebook as a Kaggle User Secret.

In the top menu bar of the notebook editor, select Add-ons then Secrets.
Create a new secret with the label GOOGLE_API_KEY.
Paste your API key into the "Value" field and click "Save".
Ensure that the checkbox next to GOOGLE_API_KEY is selected so that the secret is attached to the notebook.
3. Authenticate in the notebook

Run the cell below to access the GOOGLE_API_KEY you just saved and set it as an environment variable for the notebook to use:

# Setup: load Kaggle secret into environment

Copy the code inside braket and paste inside the kaggle cell

""" from kaggle_secrets import UserSecretsClient
import os, sys

secrets = UserSecretsClient()
try:
    key = secrets.get_secret("GOOGLE_API_KEY")  # exact name used in Kaggle Secrets UI
    os.environ["GOOGLE_API_KEY"] = key
    print("✅ Loaded GOOGLE_API_KEY into environment.")
except Exception as err:
    print("⚠️ Could not load GOOGLE_API_KEY. Running in mock mode:", err)

# Add repo src to Python path
sys.path.append('/kaggle/working/ThreatGuard-AI-Security-Agent')
sys.path.append('/kaggle/working/ThreatGuard-AI-Security-Agent/src')
print("✅ PYTHONPATH set.") """

✔ 2. Clone Your Repository Into Kaggle
Copy the code inside braket and paste inside the kaggle cell

"""!git clone https://github.com/Ashok-Kuamr/ThreatGuard-AI-Security-Agent.git"""

✔ 3. Add the Repository to PYTHONPATH
"""import sys

# Add repo root
sys.path.append('/kaggle/working/ThreatGuard-AI-Security-Agent')

# Add src folder
sys.path.append('/kaggle/working/ThreatGuard-AI-Security-Agent/src')

print("PATH updated!")"""

✔ 4. Verify Files
Copy the code inside braket and paste inside the kaggle cell

"""!ls /kaggle/working/ThreatGuard-AI-Security-Agent/src"""

✔ 5. Run the Security Engine (Main Script)

This will execute your file scanning logic.
Copy the code inside braket and paste inside the kaggle cell

"""!python /kaggle/working/ThreatGuard-AI-Security-Agent/src/main.py"""

📤 Example Output (What Judges Will See)

Your script prints system check results and file scanning behavior.
This confirms that your scanning engine works correctly directly inside Kaggle.

🧠 Notes for Judges

No API server required

No extra installation steps

No local environment

Fully reproducible in Kaggle

Main logic is in: src/main.py

Config rules are in: config/settings.yaml

This allows judges to evaluate the security logic instantly.

🏆 Why This Project Fits a Hackathon

✔ Ready-to-run
✔ Zero setup
✔ Clean structure
✔ Intelligent security analysis
✔ Clear outputs
✔ Kaggle-based reproducibility

👨‍💻 Created By

Ashok Kumar
AI & Cybersecurity Enthusiast
Building intelligent security ecosystems.

Hii Guys! I hope you like it, I created this in my exam time. I worked on it from 16 Nov 2025 to 22 Nov 2025 and my exam starts from 25 Nov. I used to study 2.5 hours for my academics and 7-8 hours for this project. In between these days my college also took mid-term exam from 17-19 Nov 2025 but I still made. For any query and problem if you face just because of mw then I am sorry. Your friend Ashok Kumar
