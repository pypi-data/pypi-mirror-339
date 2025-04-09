import os
import time
import shutil
from datetime import datetime


def run(source_folder='watched', processed_folder='processed', interval=5):
    print(f"[autodirwatchdog] Watching '{source_folder}' every {interval}s...")
    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(processed_folder, exist_ok=True)

    processed_files = set()

    while True:
        for filename in os.listdir(source_folder):
            filepath = os.path.join(source_folder, filename)
            if filename not in processed_files and os.path.isfile(filepath):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_filename = f"{timestamp}_{filename}"
                new_filepath = os.path.join(processed_folder, new_filename)
                shutil.move(filepath, new_filepath)
                print(f"[autodirwatchdog] Moved: {filename} → {new_filename}")
                processed_files.add(filename)
        time.sleep(interval)