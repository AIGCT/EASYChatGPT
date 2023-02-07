import json
import random


def getToken():

    # Open the JSON configuration file
    with open("config.json", "r") as f:
        # Parse the JSON data
        configs = json.load(f)

    # Get the list of tokens from the JSON object
    tokens = configs["apikey"]

    # Select a random token from the list 并且记录是第几个token
    n = random.randint(0, len(tokens) - 1)

    token = tokens[n]

    return token


if __name__ == "__main__":

    res = getToken()
    
    print(res)
