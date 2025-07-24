import os
import shutil
from datetime import datetime

def fetch_and_store_sysout(tracker, order_id, run_no, source_dir, archive_dir):
    try:
        source_file = f"{tracker}.LOG_{order_id}_{run_no}"
        source_path = os.path.join(source_dir, source_file)

        current_date = datetime.now().strftime('%Y%m%d')
        unique_id = f"{current_date}_{order_id}_{run_no}"
        dest_file = f"{unique_id}_{source_file}"

        # Create date-wise subdirectory under archive_dir
        datewise_dir = os.path.join(archive_dir, current_date)
        os.makedirs(datewise_dir, exist_ok=True)

        dest_path = os.path.join(datewise_dir, dest_file)

        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
            error_line = extract_error_line(dest_path)
            return error_line, dest_file
        else:
            return "Log file not found", None

    except Exception as e:
        return f"Error reading sysout: {e}", None

def extract_error_line(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if "ERROR" in line or "FAIL" in line or "NOTOK" in line:
                    return line.strip()
        return "No error found in sysout"
    except Exception as e:
        return f"Error reading log: {e}"
