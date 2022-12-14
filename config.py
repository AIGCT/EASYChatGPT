import json
import random


def getToken():

    # Open the JSON configuration file
    with open("config.json", "r") as f:
        # Parse the JSON data
        configs = json.load(f)

    # Get the list of tokens from the JSON object
    tokens = configs["session_token"]
    # cf = configs["cf_clearance"]

    # Select a random token from the list 并且记录是第几个token
    n = random.randint(0, len(tokens) - 1)
    token = tokens[n]

    # ua = configs["user_agent"]

    config = {
        "session_token": token
        # "cf_clearance": cf,
        # "user_agent": ua
    }

    return config


if __name__ == "__main__":
    print(getToken())
