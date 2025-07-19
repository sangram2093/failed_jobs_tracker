from flask import Flask, render_template, send_from_directory
from utils.sysout_fetcher import fetch_and_store_sysout
from utils.incident_fetcher import get_incident_by_job_and_order_id

app = Flask(__name__)

# Global cache for incident lookups
incident_cache = {}

@app.route("/")
def dashboard():
    file_path = "/opt/CONTROL-M/ctm/job_status.log"
    failed_jobs = []
    seen_jobs = set()  # To deduplicate based on (job_name, order_id)

    try:
        with open(file_path, 'r') as file:
            for line in file:
                if "ENDED NOTOK" in line:
                    try:
                        date = line[0:4].strip()
                        job_index = line.find('JOB ')
                        if job_index == -1:
                            continue

                        job_part = line[job_index + 4:].strip()
                        job_name = job_part.split(' (ORDERID')[0].strip()
                        order_id = job_part.split('ORDERID ')[1].split(',')[0].strip()
                        run_no = job_part.split('RUNNO ')[1].split(')')[0].strip()
                        elapsed_time = job_part.split('elapsed ')[1].split(' Sec')[0].strip()
                        cpu_time = job_part.split('cpu ')[1].split(' Sec')[0].strip()

                        # Deduplication check
                        job_key = (job_name, order_id)
                        if job_key in seen_jobs:
                            continue
                        seen_jobs.add(job_key)

                        # Sysout fetch
                        error_line, sysout_file = fetch_and_store_sysout(job_name, order_id, run_no)

                        # Incident fetch with cache check
                        if job_key in incident_cache:
                            incident_no, incident_link = incident_cache[job_key]
                        else:
                            incident_no, incident_link = get_incident_by_job_and_order_id(job_name, order_id)
                            incident_cache[job_key] = (incident_no, incident_link)

                        failed_jobs.append({
                            "time": date,
                            "tracker": job_name,
                            "OrderID": order_id,
                            "RunNo": run_no,
                            "state": "ENDED NOTOK",
                            "Elapsed Time": elapsed_time,
                            "CPU Time": cpu_time,
                            "error_line": error_line,
                            "log_file": sysout_file,
                            "incident_no": incident_no,
                            "incident_link": incident_link
                        })

                    except Exception as e:
                        print(f"Error parsing line: {line.strip()} - {e}")

    except Exception as e:
        print(f"Error reading file: {e}")

    return render_template("dashboard.html", jobs=failed_jobs)


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory('static/logs', filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
