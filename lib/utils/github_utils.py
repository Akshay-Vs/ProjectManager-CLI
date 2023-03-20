import requests
import json
import os
from sys import argv
from base64enc import encode

def upload_files(tocken, data, username, repo, filename):
    data = encode(open(data, "r").read())
    auth = tocken
    username = username
    Repo = repo
    filename = filename

    url = f"https://api.github.com/repos/{username}/{Repo}/contents/{filename}"

    payload = json.dumps({"message": f"Create {filename}", "content": f"{data}"})
    headers = {"Authorization": f"Bearer {auth}", "Content-Type": "application/json"}

    response = requests.request("PUT", url, headers=headers, data=payload)
    return {"status": response.status_code, "response": response.text}


def create_repo(tocken, name, description, private=True):
    url = "https://api.github.com/user/repos"

    payload = json.dumps(
        {"name": f"{name}", "description": f"{description}", "private": f"{private}"}
    )

    headers = {"Authorization": f"Bearer {tocken}", "Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code

if __name__ == "__main__":
    tocken = os.getenv("GITHUB_TOKEN")
    print(create_repo(tocken,"CLI-test",""))
