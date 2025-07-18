from flask import Flask, render_template, send_from_directory
from utils.parse_controlm_file import parse_controlm_log
from utils.sysout_fetcher import fetch_and_store_sysout
from utils.incident_fetcher import get_incident_by_order_id

app = Flask(__name__)

@app.route("/")
def dashboard():
    file_path = "/opt/CONTROL-M/ctm/job_status.log"
    jobs = parse_controlm_log(file_path)
    enriched_jobs = []

    for job in jobs:
        error_line, sysout_file = fetch_and_store_sysout(job['tracker'], job['OrderID'], job['RunNo'])
        incident_no, incident_link = get_incident_by_order_id(job['OrderID'])

        job.update({
            "error_line": error_line,
            "log_file": sysout_file,
            "incident_no": incident_no,
            "incident_link": incident_link
        })
        enriched_jobs.append(job)

    return render_template("dashboard.html", jobs=enriched_jobs)

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory('static/logs', filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
