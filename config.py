import json
import random
def getToken():

    # Open the JSON configuration file
    with open("config.json", "r") as f:
        # Parse the JSON data
        configs = json.load(f)

    # Get the list of tokens from the JSON object
    tokens = configs["session_token"]

    # Select a random token from the list
    token = random.choice(tokens)

    config = {
        "session_token": token
    }

    return config