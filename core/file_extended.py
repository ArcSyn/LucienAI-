# core/file_extended.py

import os, shutil, zipfile, glob

def exists(path):
    return os.path.exists(path)

def size(path):
    try:
        return f"{os.path.getsize(path)} bytes"
    except Exception as e:
        return f"⚠️ {e}"

def batch_rename(ext_from, ext_to, folder="."):
    files = glob.glob(f"{folder}/**/*{ext_from}", recursive=True)
    count = 0
    for f in files:
        new = f[: -len(ext_from)] + ext_to
        os.rename(f, new)
        count += 1
    return f"✅ Renamed {count} files."

def zip_folder(folder, zipname=None):
    zname = zipname or f"{folder}.zip"
    with zipfile.ZipFile(zname, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(folder):
            for f in files:
                z.write(os.path.join(root, f),
                        arcname=os.path.relpath(os.path.join(root, f), folder))
    return f"✅ Zipped '{folder}' → '{zname}'."

def unzip_file(zipfile_path, dest="."):
    with zipfile.ZipFile(zipfile_path, 'r') as z:
        z.extractall(dest)
    return f"✅ Unzipped '{zipfile_path}' → '{dest}'."

def replace_text(filepath, old, new):
    if not os.path.exists(filepath):
        return f"⚠️ Not found: {filepath}"
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    updated = text.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated)
    return f"✅ Replaced all '{old}' → '{new}' in {filepath}"

def count_lines(filepath):
    if not os.path.exists(filepath):
        return f"⚠️ Not found: {filepath}"
    return sum(1 for _ in open(filepath, 'r', encoding='utf-8'))

def find_large(folder, min_bytes):
    out = []
    for root, _, files in os.walk(folder):
        for f in files:
            p = os.path.join(root, f)
            if os.path.getsize(p) > min_bytes:
                out.append(p)
    return "\n".join(out) if out else f"No files > {min_bytes} bytes."