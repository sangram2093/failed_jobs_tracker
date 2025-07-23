from utils.job_parser import parse_failed_jobs
from utils.sysout_fetcher import fetch_and_store_sysout
from utils.incident_fetcher import get_incident_by_job_and_order_id
from utils.config_loader import load_config
import os
import json
from datetime import datetime

config = load_config()
output_dir = config["PATHS"]["processed_data_dir"]
sysout_src = config["PATHS"]["sysout_source_dir"]
sysout_dst = config["PATHS"]["sysout_archive_dir"]
today = datetime.now().strftime("%Y%m%d")

log_path = os.path.join(config["PATHS"]["daily_log_path"], f"daily_ctmag_{today}.log")
output_file = os.path.join(output_dir, f"{today}.json")
os.makedirs(output_dir, exist_ok=True)

# Load existing cache file for today
existing_incidents = {}
if os.path.exists(output_file):
    with open(output_file) as f:
        try:
            for job in json.load(f):
                key = (job["tracker"], job["OrderID"])
                existing_incidents[key] = job
        except Exception as e:
            print(f"[WARN] Could not parse existing JSON: {e}")

# Process today’s log
jobs = parse_failed_jobs(log_path)
final_data = []
seen_keys = set()

for job in jobs:
    key = (job["tracker"], job["OrderID"])
    if key in seen_keys:
        continue
    seen_keys.add(key)

    # Check if already in existing incident file
    if key in existing_incidents:
        final_data.append(existing_incidents[key])
        continue

    # Else fetch and store
    error_line, sysout_file = fetch_and_store_sysout(job["tracker"], job["OrderID"], job["RunNo"], sysout_src, sysout_dst)
    incident_no, incident_link = get_incident_by_job_and_order_id(job["tracker"], job["OrderID"], config)

    job.update({
        "error_line": error_line,
        "log_file": sysout_file,
        "incident_no": incident_no,
        "incident_link": incident_link
    })
    final_data.append(job)

# Save output file
with open(output_file, "w") as f:
    json.dump(final_data, f, indent=2)