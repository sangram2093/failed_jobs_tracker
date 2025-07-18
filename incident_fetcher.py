import requests

SERVICENOW_API_URL = "https://<servicenow_instance>.service-now.com/api/now/table/incident"
AUTH = ('username', 'password')  # Use secrets manager in prod

def get_incident_by_order_id(order_id):
    try:
        params = {
            'sysparm_query': f'u_order_id={order_id}',
            'sysparm_limit': 1
        }
        response = requests.get(SERVICENOW_API_URL, auth=AUTH, params=params)
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
