import os
import shutil
from datetime import datetime

SYSOUT_SOURCE_DIR = "/opt/CONTROL-M/ctm/sysout"
SYSOUT_ARCHIVE_DIR = "./static/logs"

def fetch_and_store_sysout(tracker, order_id, run_no):
    try:
        source_file = f"{tracker}.LOG_{order_id}_{run_no}"
        source_path = os.path.join(SYSOUT_SOURCE_DIR, source_file)

        unique_id = f"{datetime.now().strftime('%Y%m%d')}_{order_id}_{run_no}"
        dest_file = f"{unique_id}_{source_file}"
        dest_path = os.path.join(SYSOUT_ARCHIVE_DIR, dest_file)

        if not os.path.exists(SYSOUT_ARCHIVE_DIR):
            os.makedirs(SYSOUT_ARCHIVE_DIR)

        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
            error_line = extract_error_line(dest_path)
            return error_line, dest_file
        else:
            return "Log file not found", None

    except Exception as e:
        return f"Error reading sysout: {e}", None

def extract_error_line(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if "ERROR" in line or "FAIL" in line or "NOTOK" in line:
                return line.strip()
    return "No error found in sysout"
