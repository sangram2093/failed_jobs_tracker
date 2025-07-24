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
    """
    Extracts a snippet of 10 lines before and after the first occurrence of an error keyword.
    Searches for keywords like 'error', 'fail', 'failed', 'notok' in any casing.
    """
    error_keywords = ["error", "fail", "failed", "notok"]
    try:
        with open(file_path, 'r', errors='ignore') as file:
            lines = file.readlines()

        for idx, line in enumerate(lines):
            lower_line = line.lower()
            if any(keyword in lower_line for keyword in error_keywords):
                start_idx = max(0, idx - 10)
                end_idx = min(len(lines), idx + 11)  # +11 to include current + 10 lines
                error_snippet = lines[start_idx:end_idx]
                return ''.join(error_snippet).strip()

        return "No recognizable error found in sysout"

    except Exception as e:
        return f"Error reading log: {e}"
