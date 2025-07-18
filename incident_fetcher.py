import requests

SERVICENOW_API_URL = "https://<servicenow_instance>.service-now.com/api/now/table/incident"
AUTH = ('username', 'password')  # Replace with credentials or use a token

PROXIES = {
    "http": "http://<proxy_host>:<proxy_port>",
    "https": "http://<proxy_host>:<proxy_port>"
}

def get_incident_by_job_and_order_id(job_name, order_id):
    try:
        # Example: descriptionLIKE<job_name>^descriptionLIKE<order_id>
        query = f"descriptionLIKE{job_name}^descriptionLIKE{order_id}"

        params = {
            'sysparm_query': query,
            'sysparm_limit': 1
        }

        response = requests.get(
            SERVICENOW_API_URL,
            auth=AUTH,
            params=params,
            proxies=PROXIES,
            verify=False   # Disable if required (but better to keep SSL verification enabled)
        )
        response.raise_for_status()

        incidents = response.json().get('result', [])
        if incidents:
            incident_number = incidents[0].get('number')
            incident_sys_id = incidents[0].get('sys_id')
            incident_link = f"https://<servicenow_instance>.service-now.com/nav_to.do?uri=incident.do?sys_id={incident_sys_id}"
            return incident_number, incident_link
        else:
            return "No Incident Found", "#"

    except Exception as e:
        return f"Error: {e}", "#"
