from flask import Flask, render_template, request
import os, json
from datetime import datetime, timedelta
from utils.config_loader import load_config

app = Flask(__name__)
config = load_config()

@app.route("/", methods=["GET"])
def dashboard():
    data_dir = config["PATHS"]["processed_data_dir"]
    today = datetime.now().strftime("%Y%m%d")
    selected_date = request.args.get("date", today)
    data_file = os.path.join(data_dir, f"{selected_date}.json")

    jobs = []
    if os.path.exists(data_file):
        with open(data_file) as f:
            jobs = json.load(f)

    # Populate dropdown from available JSON files
    available_dates = sorted([
        f.replace(".json", "") for f in os.listdir(data_dir)
        if f.endswith(".json")
    ], reverse=True)

    # Count trend for last 7 days
    trend = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y%m%d")
        file = os.path.join(data_dir, f"{date}.json")
        if os.path.exists(file):
            with open(file) as f:
                count = len(json.load(f))
                trend.append({"date": date, "count": count})
    trend = list(reversed(trend))  # oldest to newest

    return render_template("dashboard.html", jobs=jobs, dates=available_dates, selected=selected_date, trend=trend)
