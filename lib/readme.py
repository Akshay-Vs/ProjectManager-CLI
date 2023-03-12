import requests
import json
import logging
import os
from datetime import date

logging.basicConfig(
    filename="readme.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def get_template(path="README.md"):
    try:
        logging.info("Downloading Template")
        return requests.get(
            "https://raw.githubusercontent.com/Akshay-Vs/templates/master/README/Black-Night.md",
            allow_redirects=True,
        ).content
    except Exception as e:
        return e


def generate_readme(token, user, repo):
    logging.info("Generating Readme")

    Readme = get_template().decode("utf-8")
    logging.info("Downloading Template")

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.request(
        "GET", f"https://api.github.com/repos/{user}/{repo}", headers=headers
    )
    response = json.loads(response.text)
    # print(response)
    logging.info("Writing Contents")

    user = response["owner"]["login"]
    repo = response["name"]
    description = response["description"]
    avatar = response["owner"]["avatar_url"]

    # languages
    language = response["languages_url"]
    language = requests.request("GET", language)
    language = json.loads(language.text)
    Readme = Readme.replace("{User}", user)
    Readme = Readme.replace("{Repo}", repo)
    Readme = Readme.replace("{Description}", description)
    Readme = Readme.replace("{Avatar}", avatar)
    Readme = Readme.replace("{Year}", f"{date.today().year}")

    if response["license"] != None:
        license = response["license"]["name"]
        Readme = Readme.replace("{License}", license)

    if len(language) > 1:
        primary_language = list(language)[0]
        secondary_language = list(language)[1]
        Readme = Readme.replace("{Primary Language}", primary_language)
        Readme = Readme.replace("{Version}", "0.0")
        Readme = Readme.replace("{Secondary language}", secondary_language)
        with open("README.md", "w+") as f:
            f.write(Readme)
    logging.info("Generated Readme.md from Black-Night template")


if __name__ == "__main__":
    generate_readme(os.getenv("GITHUB_TOKEN"), "Akshay-Vs", "Passlock")
