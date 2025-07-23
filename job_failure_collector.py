import os
import json
from datetime import datetime
from utils.config_loader import load_config
from utils.job_parser import parse_failed_jobs
from utils.incident_fetcher import get_incident_by_job_and_order_id
from utils.sysout_fetcher import fetch_and_store_sysout

config = load_config()
log_dir = config["PATHS"]["daily_log_path"]
sysout_src = config["PATHS"]["sysout_source_dir"]
sysout_dst = config["PATHS"]["sysout_archive_dir"]
output_dir = config["PATHS"]["processed_data_dir"]

today = datetime.now().strftime("%Y%m%d")
log_file = os.path.join(log_dir, f"daily_ctmag_{today}.log")
output_file = os.path.join(output_dir, f"{today}.json")

os.makedirs(output_dir, exist_ok=True)
jobs = parse_failed_jobs(log_file)

seen_keys = set()
output_data = []

for job in jobs:
    key = (job['tracker'], job['OrderID'])
    if key in seen_keys:
        continue
    seen_keys.add(key)

    error_line, sysout_file = fetch_and_store_sysout(job['tracker'], job['OrderID'], job['RunNo'], sysout_src, sysout_dst)
    incident_no, incident_link = get_incident_by_job_and_order_id(job['tracker'], job['OrderID'], config)

    job.update({
        "error_line": error_line,
        "log_file": sysout_file,
        "incident_no": incident_no,
        "incident_link": incident_link
    })
    output_data.append(job)

with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=2)
