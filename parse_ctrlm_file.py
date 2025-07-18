import re

def parse_controlm_log(file_path):
    failed_jobs = []

    # Regex pattern to extract required details
    pattern = re.compile(
        r"""
        ^\d{4}\s+\d+\s+\d+\s+\w+\s+JOB\s+(?P<tracker>[\w\.\-]+)\s+
        \(ORDERID\s+(?P<order_id>[\w\d]+),\s+RUNNO\s+(?P<run_no>\d+)\)\s+
        (?P<state>ENDED\s+NOTOK).*?
        elapsed\s+(?P<elapsed>[\-\d\.]+)\s+Sec\s+
        cpu\s+(?P<cpu>[\-\d\.]+)\s+Sec
        """,
        re.VERBOSE
    )

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
                    "time": line[:4]  # MMDD from the line start
                })

    return failed_jobs
