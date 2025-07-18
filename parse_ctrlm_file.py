import re

def parse_controlm_log(file_path):
    failed_jobs = []

    pattern = re.compile(
        r"""
        ^(?P<date>\d{4})\s+\d+\s+\d+\s+\w+\s+JOB\s+(?P<tracker>[\w\.\-]+)\s+
        \(ORDERID\s+(?P<order_id>[\w\d]+),\s+RUNNO\s+(?P<run_no>\d+)\)\s+
        (?P<state>ENDED\s+NOTOK).*?
        elapsed\s+(?P<elapsed>[\-\d\.]+)\s+Sec\s+
        cpu\s+(?P<cpu>[\-\d\.]+)\s+Sec
        """,
        re.VERBOSE
    )

    try:
        with open(file_path, 'r') as file:
            for line in file:
                match = pattern.search(line)
                if match:
                    failed_jobs.append({
                        "tracker": match.group('tracker'),
                        "OrderID": match.group('order_id'),
                        "RunNo": match.group('run_no'),
                        "state": "ENDED NOTOK",
                        "Elapsed Time": match.group('elapsed'),
                        "CPU Time": match.group('cpu'),
                        "time": match.group('date')  # MMDD format
                    })
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error parsing file: {e}")

    return failed_jobs
