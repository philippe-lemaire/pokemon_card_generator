import requests
import pandas as pd

api_file = "../../api-key/key"

base_uri = "https://api.pokemontcg.io/v2/"


def get_file_contents(filename):
    """Given a filename,
    return the contents of that file
    """
    try:
        with open(filename, "r") as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)


my_key = get_file_contents(api_file)
headers = {"X-Api-Key": my_key}


def get_sets():
    """queries the pokemontgc api and returns a dataframe with all the sets data."""
    params = {"q": "", "orderBy": "releaseDate"}
    endpoint = "sets/"
    url = base_uri + endpoint
    sets = requests.get(url, params=params, headers=headers).json()["data"]
    sets_df = pd.DataFrame(sets)
    return sets_df
