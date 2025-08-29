# core/system_extended.py

import os, psutil, subprocess, webbrowser, random, string

def disk_space():
    d = psutil.disk_usage(os.getcwd())
    return f"📂 Total {d.total // 2**30} GB, Free {d.free // 2**30} GB, Used {d.percent}%"

def cpu_usage():
    return f"🧠 CPU Usage: {psutil.cpu_percent(interval=1)}%"

def shell(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return f"⛭ STDOUT:\n{r.stdout}\n⛭ STDERR:\n{r.stderr}"
    except Exception as e:
        return f"⚠️ {e}"

def rand_pass(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def open_url(url):
    try:
        webbrowser.open(url)
        return f"✅ Opened URL: {url}"
    except Exception as e:
        return f"⚠️ {e}"

def open_file_in_vscode(path):
    try:
        subprocess.run(["code", path], check=True)
        return f"✅ Opened in VS Code: {path}"
    except Exception as e:
        return f"⚠️ {e}"