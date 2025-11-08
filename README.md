🖥️ Server Health Monitoring System
⚡ Real-Time System Monitoring with Streamlit Dashboard + Telegram Alerts + SQLite Storage
📘 Overview

This project is a complete real-time server monitoring system built using Python.
It continuously tracks your CPU, Memory, Disk, and Network usage, logs everything into a local database (SQLite),
and automatically sends Telegram alerts when any system resource crosses the defined threshold.

It also includes a beautiful Streamlit dashboard that visualizes data using Plotly charts,
and provides options to download logs in CSV or JSON formats.

Perfect for:

Students showcasing Python + DevOps skills

System admins wanting lightweight monitoring

Resume projects to demonstrate automation, data visualization, and API integration

🧱 Architecture
System → psutil → SQLite Database → Streamlit Dashboard
                      ↓
                Telegram Alerts

🚀 Key Features :

✅ Real-time tracking of CPU, Memory, Disk, and Network
✅ Alerts via Telegram Bot for high usage
✅ Auto logs to SQLite, CSV, and Excel
✅ Interactive Streamlit dashboard with live charts
✅ Download logs as CSV or JSON
✅ Configurable thresholds and intervals via config.json
✅ Auto-export every minute
✅ Clean, modular, and GitHub-ready structure

🧩 Project Structure
📁 server_monitoring_project/
│
|  config
│   ├── server_monitor.log               # Runtime logs
│   ├── server_data.db                   # SQLite database
│   ├── server_log.csv                   # Auto-generated CSV export
│   └── server_log.xlsx                  # Auto-generated Excel export
│
├── 📂 dashboard/
│   ├── dashboard.py                     # Streamlit dashboard visualization
│   └── assets/                          # (Optional) Custom CSS, logos
│
├── 📂 reports/                          # (Optional) For future PDF/CSV reports
│
├── requirements.txt                     # Python dependencies
└── README.md                            # Documentation (this file)

⚙️ System Requirements

Component	Version / Tool

Python	3.11 or 3.12 ✅

Streamlit	1.39.0

SQLite	(Built-in with Python)

OS	Windows / Linux / macOS

Telegram App	Installed on your phone

📦 Installation & Setup

🪶 Step 1 — Clone the Repository

git clone https://github.com/<your-username>/server_monitoring_project.git
cd server_monitoring_project

🪶 Step 2 — Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # (Windows)
# or
source venv/bin/activate  # (Linux/Mac)

🪶 Step 3 — Install Requirements
pip install -r requirements.txt

🪶 Step 4 — Create Telegram Bot

You’ll need a Telegram bot for alert notifications.

🧠 How to create your Telegram bot:

Open Telegram App

Search for @BotFather and start a chat

Send the command:

/newbot

BotFather will ask for a name and username (e.g., ServerMonitorBot)

You’ll receive a message containing your Bot Token, like:

8360785161:AAHiepJ3Pdj2NCSQhDS9l_O5c8FwYz-WBCY

Save this token — it’s your BOT_TOKEN.

🧩 Get your Chat ID:

Open your new bot on Telegram and click Start

Visit this URL in your browser (replace <BOT_TOKEN>):

https://api.telegram.org/bot<BOT_TOKEN>/getUpdates


You’ll get JSON output — look for:

"chat": {"id": 123456789, "first_name": "Vishal"}


Copy the numeric value as your CHAT_ID.

🪶 Step 5 — Run the Monitor
 
python monitor_telegram_advanced.py


✅ This will:

Log system stats every minute

Save to server_data.db

Export server_log.csv

Send Telegram alerts on high usage

🪶 Step 6 — Launch the Dashboard

Open another terminal and run:

cd dashboard
python -m streamlit run dashboard.py


Visit the dashboard in your browser:

http://localhost:8501


You’ll see:

CPU, Memory, Disk indicators

Upload/Download charts

Data download buttons


📊 Dashboard Preview

Feature	Description

🧠 System Usage	Real-time CPU, RAM, Disk visualization
🌐 Network Activity	Upload/Download MB trend line chart
📥 Data Download	CSV / JSON export buttons
🕒 Auto Refresh	Updates every few seconds
⚙️ Sidebar Controls	Refresh speed slider

🧠 Behind the Scenes

Module	Function
psutil	Fetch system performance metrics
sqlite3	Store readings in a local DB
requests	Send Telegram notifications
pandas	Data manipulation and export
plotly	Interactive data visualization
streamlit	Dashboard and UI rendering

📈 Example Telegram Alert

⚠️ Server Alert: High Usage
CPU Usage: 88% (Limit: 80%)
Memory Usage: 79% (Limit: 75%)
Disk Usage: 67% (Limit: 85%)
Network Sent: 13.54 MB
Network Received: 27.18 MB

🧩 Usage Flow

1️⃣ Start monitor_telegram_advanced.py
2️⃣ It collects stats every minute
3️⃣ Saves data in server_data.db
4️⃣ Triggers Telegram alert if limits exceed
5️⃣ Streamlit dashboard visualizes everything live

💾 Database Schema

SQLite file: server_data.db

Column	Type	Description
time	TEXT	Timestamp
cpu	REAL	CPU usage (%)
memory	REAL	Memory usage (%)
disk	REAL	Disk usage (%)
sent	REAL	Network upload (MB)
recv	REAL	Network download (MB)
