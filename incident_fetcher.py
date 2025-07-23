import requests

def get_incident_by_job_and_order_id(job_name, order_id, config):
    try:
        # Build query string for ServiceNow API
        query = f"descriptionLIKE{job_name}^descriptionLIKE{order_id}"
        params = {
            'sysparm_query': query,
            'sysparm_limit': 1
        }

        servicenow_url = config["SERVICENOW"]["url"]
        auth = (
            config["SERVICENOW"]["username"],
            config["SERVICENOW"]["password"]
        )

        proxies = {
            "http": config["SERVICENOW"]["proxy"]["http"],
            "https": config["SERVICENOW"]["proxy"]["https"]
        }

        response = requests.get(
            servicenow_url,
            auth=auth,
            params=params,
            proxies=proxies,
            verify=False  # You can make this configurable too
        )
        response.raise_for_status()

        incidents = response.json().get('result', [])
        if incidents:
            incident_number = incidents[0].get('number')
            incident_sys_id = incidents[0].get('sys_id')

            # Build incident URL dynamically from base URL
            base_url = servicenow_url.split("/api")[0]
            incident_link = f"{base_url}/nav_to.do?uri=incident.do?sys_id={incident_sys_id}"

            return incident_number, incident_link
        else:
            return "No Incident Found", "#"

    except Exception as e:
        return f"Error: {e}", "#"
