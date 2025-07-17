from flask import Flask, render_template, send_from_directory
from utils.fetch_geneos import fetch_geneos_data
from utils.fetch_sysout import process_sysout
from utils.fetch_incident import get_incident
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    url = "http://geneos-hosted-services-uk.flgd.cd.com:20431/@@/ALL+OTHER+ENVIRONMENT/PROD/ControlM+Job+State+V9.htm"
    jobs = fetch_geneos_data(url)
    failed_jobs = []

    for job in jobs:
        if job.get('state') == "ENDED NOTOK":
            unique_id, error_line, file_name = process_sysout(
                job.get('tracker'), job.get('OrderID'), job.get('RunNo')
            )
            incident_no, incident_link = get_incident(job.get('OrderID'))
            failed_jobs.append({
                "tracker": job.get('tracker'),
                "state": job.get('state'),
                "time": job.get('time'),
                "OrderID": job.get('OrderID'),
                "RunNo": job.get('RunNo'),
                "Elapsed Time": job.get('Elapsed Time'),
                "CPU Time": job.get('CPU Time'),
                "unique_id": unique_id,
                "error": error_line,
                "incident_no": incident_no,
                "incident_link": incident_link,
                "log_file": file_name
            })

    return render_template("dashboard.html", jobs=failed_jobs)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('static/logs', filename, as_attachment=True)

if __name__ == "__main__":
    os.makedirs('./static/logs', exist_ok=True)
    app.run(debug=True, host="0.0.0.0", port=5000)
