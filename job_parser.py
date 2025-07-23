# utils/job_parser.py

def parse_failed_jobs(file_path):
    failed_jobs = []
    seen = set()

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

                        key = (job_name, order_id)
                        if key in seen:
                            continue
                        seen.add(key)

                        failed_jobs.append({
                            "time": date,
                            "tracker": job_name,
                            "OrderID": order_id,
                            "RunNo": run_no,
                            "state": "ENDED NOTOK",
                            "Elapsed Time": elapsed_time,
                            "CPU Time": cpu_time
                        })
                    except Exception as e:
                        print(f"[ParseError] Line skipped: {line.strip()} | {e}")
    except Exception as e:
        print(f"[FileReadError] Could not read {file_path}: {e}")

    return failed_jobs
