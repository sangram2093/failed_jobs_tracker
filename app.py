from flask import Flask, render_template, request, send_from_directory
import os
import json
from datetime import datetime, timedelta
from utils.config_loader import load_config

app = Flask(__name__)
config = load_config()

@app.route("/", methods=["GET"])
def dashboard():
    data_dir = config["PATHS"]["processed_data_dir"]
    sysout_dir = config["PATHS"]["sysout_archive_dir"]

    # Get date from dropdown or default to today
    today = datetime.now().strftime("%Y%m%d")
    selected_date = request.args.get("date", today)
    data_file = os.path.join(data_dir, f"{selected_date}.json")

    # Load selected day's jobs
    jobs = []
    if os.path.exists(data_file):
        with open(data_file) as f:
            jobs = json.load(f)
        # Add log_date to each job for download routing
        for job in jobs:
            job["log_date"] = selected_date

    # Prepare dropdown options based on available files
    available_dates = sorted([
        f.replace(".json", "") for f in os.listdir(data_dir)
        if f.endswith(".json")
    ], reverse=True)

    # Generate 7-day incident count trend
    trend = []
    for i in range(7):
        day = (datetime.now() - timedelta(days=i)).strftime("%Y%m%d")
        file = os.path.join(data_dir, f"{day}.json")
        count = 0
        if os.path.exists(file):
            with open(file) as f:
                count = len(json.load(f))
        trend.append({"date": day, "count": count})
    trend = list(reversed(trend))  # oldest to newest

    return render_template("dashboard.html",
                           jobs=jobs,
                           dates=available_dates,
                           selected=selected_date,
                           trend=trend)

@app.route("/download/<log_date>/<filename>")
def download_file(log_date, filename):
    # Serve log file from the date-wise archive subfolder
    date_folder = os.path.join(config["PATHS"]["sysout_archive_dir"], log_date)
    return send_from_directory(date_folder, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
