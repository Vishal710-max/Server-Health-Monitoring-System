"""
dashboard.py
Enhanced Streamlit dashboard with:
✅ Live system stats
✅ Professional charts
✅ Download CSV/JSON options
"""

import streamlit as st
import psutil
import pandas as pd
import time
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime


# ===== PAGE SETUP =====
st.set_page_config(page_title="Server Monitor Dashboard", layout="wide")

# ===== HEADER =====
st.title("🖥️ Server Health Monitor Dashboard")
st.markdown("Real-time system stats + professional charts + file export options")

# ===== LIVE METRICS =====
col1, col2, col3 = st.columns(3)

with col1:
    cpu = psutil.cpu_percent(interval=1)
    st.metric("🧠 CPU Usage", f"{cpu} %")

with col2:
    mem = psutil.virtual_memory().percent
    st.metric("💾 Memory Usage", f"{mem} %")

with col3:
    disk = psutil.disk_usage('/').percent
    st.metric("📀 Disk Usage", f"{disk} %")

st.progress(cpu / 100)
st.progress(mem / 100)
st.progress(disk / 100)

st.divider()

# ===== LOAD DATA =====
st.subheader("📈 Performance Overview")

try:
    import sqlite3
    conn = sqlite3.connect("server_data.db")
    df = pd.read_sql("SELECT * FROM stats ORDER BY time DESC LIMIT 100", conn)
    conn.close()

    df["time"] = pd.to_datetime(df["time"])

    # ===== SYSTEM USAGE CHARTS =====
    st.subheader("🧠 System Resource Usage")
    chart_type = st.radio("📊 Select Chart Type:", ["Line Chart", "Bar Chart"], horizontal=True)

    if chart_type == "Line Chart":
        fig = px.line(df, x="time", y=["cpu", "memory", "disk"], markers=True,
                      title="System Resource Usage Over Time")
        fig.update_layout(template="plotly_dark", xaxis_title="Time", yaxis_title="Usage (%)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.bar(df.tail(10), x="time", y=["cpu", "memory", "disk"], barmode="group",
                     title="Last 10 Readings (Grouped View)")
        fig.update_layout(template="plotly_dark", xaxis_title="Time", yaxis_title="Usage (%)")
        st.plotly_chart(fig, use_container_width=True)

    # ===== NETWORK USAGE CHART =====
    st.divider()
    st.subheader("🌐 Network Activity (MB Transferred)")

    fig_net = px.line(df, x="time", y=["sent", "recv"], markers=True,
                      title="Network Upload & Download Trend")
    fig_net.update_layout(
        template="plotly_dark",
        xaxis_title="Time",
        yaxis_title="Megabytes (MB)",
        legend_title="Direction"
    )
    st.plotly_chart(fig_net, use_container_width=True)

    # ===== DOWNLOAD OPTIONS =====
    st.divider()
    st.subheader("📥 Download Data")

    csv_data = df.to_csv(index=False).encode('utf-8')
    json_data = df.to_json(orient='records', indent=2).encode('utf-8')

    colA, colB = st.columns(2)
    with colA:
        st.download_button("⬇️ Download CSV", csv_data, "server_data.csv", "text/csv")
    with colB:
        st.download_button("⬇️ Download JSON", json_data, "server_data.json", "application/json")

    st.success("✅ Data loaded from database successfully!")

except Exception as e:
    st.error(f"❌ Failed to load data: {e}")


    # ===== VISUALIZATION SECTION =====
    chart_type = st.radio("📊 Select Chart Type:", ["Line Chart", "Bar Chart"], horizontal=True)

    if chart_type == "Line Chart":
        fig = px.line(df, x="Time", y=["CPU", "Memory", "Disk"], markers=True,
                      title="System Resource Usage Over Time")
        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Timestamp",
            yaxis_title="Usage (%)",
            legend_title="Metric"
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        latest_df = df.tail(10)  # last 10 readings
        fig = px.bar(latest_df, x="Time", y=["CPU", "Memory", "Disk"],
                     barmode="group", title="Last 10 Readings (Grouped View)")
        fig.update_layout(template="plotly_dark", xaxis_title="Timestamp", yaxis_title="Usage (%)")
        st.plotly_chart(fig, use_container_width=True)

    # ===== DOWNLOAD OPTIONS =====
    st.divider()
    st.subheader("📥 Download Logs")

    colA, colB = st.columns(2)

    csv_data = df.to_csv(index=False).encode('utf-8')
    json_data = df.to_json(orient='records', indent=2).encode('utf-8')

    with colA:
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name=f"server_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime='text/csv'
        )

    with colB:
        st.download_button(
            label="⬇️ Download JSON",
            data=json_data,
            file_name=f"server_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime='application/json'
        )

    st.success("✅ Data ready for download and visualization updated successfully.")

except FileNotFoundError:
    st.warning("⚠️ `server_log.csv` not found. Please run your monitor script first.")

# ===== LAST ALERT TIME =====
st.divider()
try:
    with open("server_monitor.log", "r") as log_file:
        lines = log_file.readlines()
        alerts = [l for l in lines if "Telegram alert sent" in l]
        if alerts:
            last_alert = alerts[-1].split(":")[0] + ":" + alerts[-1].split(":")[1]
            st.info(f"🕒 Last Alert Sent At: {last_alert}")
        else:
            st.info("No alerts sent yet.")
except FileNotFoundError:
    st.warning("`server_monitor.log` not found.")

# ===== AUTO REFRESH =====
st.sidebar.header("⚙️ Auto Refresh Settings")
refresh_sec = st.sidebar.slider("Refresh interval (seconds)", 5, 60, 10)
st.sidebar.write(f"Dashboard updates every {refresh_sec} seconds")

time.sleep(refresh_sec)
st.rerun()
