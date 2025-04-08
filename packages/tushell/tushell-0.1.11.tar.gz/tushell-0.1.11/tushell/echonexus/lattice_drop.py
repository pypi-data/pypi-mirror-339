import requests

def fetch_echonode_data():
    url = "https://edgehub.click/api/echonode"
    headers = {
        "Authorization": "Bearer ITERAX_TOKEN"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def process_echonode_data(data):
    # Process the data as needed
    return data

def render_echonode_data(data):
    # Render the data as part of the memory key graph
    for key, value in data.items():
        print(f"{key}: {value}")
