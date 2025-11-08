"""
monitor_telegram_advanced.py
Author: Vishal Bhingarde
Description:
Advanced Server Monitor with Telegram Alerts, Live CSV Export (every 10 mins),
and Daily Summary for Streamlit Dashboard.
"""
import sqlite3
import psutil
import requests
import time
import logging
import pandas as pd
from datetime import datetime, timedelta

# ====== CONFIG SETTINGS ======
CPU_THRESHOLD = 80        # percent
MEMORY_THRESHOLD = 75     # percent
DISK_THRESHOLD = 85       # percent
CHECK_INTERVAL = 60      # seconds (1 minutes)

BOT_TOKEN = "8360785161:AAHiepJ3Pdj2NCSQhDS9l_O5c8FwYz-WBCY"
CHAT_ID = "7072105746"         # Replace with your chat id

LOG_FILE = "server_monitor.log"

# ====== LOGGING SETUP ======
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# ====== GLOBAL VARIABLES ======
daily_stats = {"cpu": [], "memory": [], "disk": []}
last_summary_time = datetime.now()
last_csv_export = datetime.now()   # <--- new variable

# ====== FUNCTION: Send Telegram Message ======
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, data=payload)
        logging.info("Telegram alert sent.")
    except Exception as e:
        logging.error(f"Telegram alert failed: {e}")

# ====== FUNCTION: Export Logs ======
def export_logs_to_csv():
    try:
        rows = []
        with open(LOG_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(':', 2)  # split only 2 times
                if len(parts) == 3:
                    time_str, level, message = parts
                    rows.append([time_str, level, message])
                else:
                    continue  # skip malformed lines

        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=['Time', 'Level', 'Message'])
        df.to_csv('server_log.csv', index=False)
        df.to_excel('server_log.xlsx', index=False)
        logging.info("Logs exported to CSV and Excel successfully.")
    except Exception as e:
        logging.error(f"Error exporting logs: {e}")

# ====== FUNCTION: Save to SQLite Database ======
def save_to_database(cpu, memory, disk, sent_mb, recv_mb):
    try:
        conn = sqlite3.connect("server_data.db")
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                time TEXT,
                cpu REAL,
                memory REAL,
                disk REAL,
                sent REAL,
                recv REAL
            )
        """)
        cur.execute("INSERT INTO stats VALUES (?, ?, ?, ?, ?, ?)",
                    (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cpu, memory, disk, sent_mb, recv_mb))
        conn.commit()
        conn.close()
        logging.info("Saved system stats to SQLite database.")
    except Exception as e:
        logging.error(f"Database insert failed: {e}")


# ====== FUNCTION: Check System Resources ======
def check_system_resources():
    global daily_stats, last_summary_time, last_csv_export

    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    net_io = psutil.net_io_counters()
    sent_mb = net_io.bytes_sent / (1024 * 1024)
    recv_mb = net_io.bytes_recv / (1024 * 1024)

    #logging.info(f"CPU: {cpu}%, Memory: {memory}%, Disk: {disk}%, Sent: {sent_mb:.2f}MB, Received: {recv_mb:.2f}MB")
    save_to_database(cpu, memory, disk, sent_mb, recv_mb)

    # Alert condition
    if cpu > CPU_THRESHOLD or memory > MEMORY_THRESHOLD or disk > DISK_THRESHOLD:
        message = (f"⚠️ *Server Alert: High Usage*\n\n"
                   f"CPU Usage: {cpu}% (Limit: {CPU_THRESHOLD}%)\n"
                   f"Memory Usage: {memory}% (Limit: {MEMORY_THRESHOLD}%)\n"
                   f"Disk Usage: {disk}% (Limit: {DISK_THRESHOLD}%)\n"
                   f"Network Sent: {sent_mb:.2f} MB\n"
                   f"Network Received: {recv_mb:.2f} MB")
        send_telegram_message(message)

    # Track data for daily summary
    daily_stats["cpu"].append(cpu)
    daily_stats["memory"].append(memory)
    daily_stats["disk"].append(disk)

    # --- AUTO EXPORT LOGS EVERY 1 MINUTES ---
    if datetime.now() - last_csv_export >= timedelta(minutes=1):
        export_logs_to_csv()
        last_csv_export = datetime.now()

    # --- DAILY SUMMARY (every 24 hours) ---
    if datetime.now() - last_summary_time >= timedelta(hours=24):
        avg_cpu = sum(daily_stats["cpu"]) / len(daily_stats["cpu"])
        avg_mem = sum(daily_stats["memory"]) / len(daily_stats["memory"])
        avg_disk = sum(daily_stats["disk"]) / len(daily_stats["disk"])

        summary = (f"📅 *Daily Server Summary*\n\n"
                   f"Avg CPU: {avg_cpu:.2f}%\n"
                   f"Avg Memory: {avg_mem:.2f}%\n"
                   f"Avg Disk: {avg_disk:.2f}%\n"
                   f"Entries Recorded: {len(daily_stats['cpu'])}")
        send_telegram_message(summary)
        export_logs_to_csv()
        daily_stats = {"cpu": [], "memory": [], "disk": []}
        last_summary_time = datetime.now()

# ====== MAIN LOOP ======
if __name__ == "__main__":
    logging.info("🚀 Advanced Telegram Server Monitor started.")
    while True:
        check_system_resources()
        time.sleep(CHECK_INTERVAL)
