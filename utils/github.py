import requests
import json

def createRepo(url, headers, data):
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.status_code

def getRepo(url, headers):
    requests = requests.get(url, headers=headers)
    return requests.json()