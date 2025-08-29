# system_ops.py

import psutil
import datetime
import webbrowser
import os
import subprocess

def get_system_info():
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        now = datetime.datetime.now()

        info = [
            f"🖥️ CPU Usage: {cpu_percent}%",
            f"🧠 RAM Usage: {ram.percent}%",
            f"💾 Disk Usage: {disk.percent}%",
            f"⏰ Current Time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
        ]
        return "\n".join(info)
    except Exception as e:
        return f"⚠️ Error getting system info: {e}"


def open_url(url):
    try:
        webbrowser.open(url)
        return f"✅ Opened URL: {url}"
    except Exception as e:
        return f"⚠️ Error opening URL: {e}"


def open_file_in_vscode(filepath):
    try:
        subprocess.run(["code", filepath], check=True)
        return f"✅ Opened {filepath} in VS Code."
    except Exception as e:
        return f"⚠️ Error opening file in VS Code: {e}"