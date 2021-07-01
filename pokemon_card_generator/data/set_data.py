import requests
import pandas as pd
from os import walk, path
from pokemon_card_generator import utils


three_dirs_up = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

api_file = path.join(three_dirs_up, "pokemontcg_api_key/key")

base_uri = "https://api.pokemontcg.io/v2/"


my_key = utils.get_file_contents(api_file)
headers = {"X-Api-Key": my_key}


def download_sets():
    """queries the pokemontgc api and returns a dataframe with all the sets data."""
    params = {"q": "", "orderBy": "releaseDate"}
    endpoint = "sets/"
    url = base_uri + endpoint
    sets = requests.get(url, params=params, headers=headers).json()["data"]
    sets_df = pd.DataFrame(sets)
    sets_df.releaseDate = pd.to_datetime(sets_df.releaseDate)
    return sets_df


def get_sets():
    ## get sets using the pickle
    three_dirs_up = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
    sets_pickle_path = path.join(three_dirs_up, "raw_data/sets_pickle/sets.pickle")
    sets_df = pd.read_pickle(sets_pickle_path)
    return sets_df


if __name__ == "main":
    print(api_file)
