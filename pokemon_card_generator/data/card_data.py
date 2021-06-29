import csv
import pandas as pd
from pokemon_card_generator.data.set_data import get_sets


def get_card_data():
    """Concatenates all the pickles in 'raw_data/pickles' and returns a dataframe.
    Usage: from pokemon_card_generator.data import card_data; card_df = card_data.get_card_data()"""
    # list all the files in data
    from os import walk, path

    two_dirs_up = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

    pickles_path = path.join(two_dirs_up, "raw_data/pickles")

    filenames = next(walk(pickles_path), (None, None, []))[2]  # [] if no file

    # create a final df with first pickles
    cards_df = pd.read_pickle(path.join(pickles_path, filenames[0]))
    # open each other pickle and stack it into the final df
    for file in filenames[1:]:
        filepath = path.join(pickles_path, file)
        temp_df = pd.read_pickle(filepath)

        cards_df = pd.concat([cards_df, temp_df.reset_index()], axis=0)

    cards_df.reset_index(inplace=True)
    cards_df.drop(columns=["level_0"], inplace=True)

    ## add release dates in a new column
    sets_df = get_sets()
    release_date_dict = {k: v for k, v in zip(sets_df.id, sets_df.releaseDate)}
    card_sets = [row["id"].split("-")[0] for _, row in cards_df.iterrows()]
    card_release_dates = pd.Series([release_date_dict[set_] for set_ in card_sets])
    cards_df["releaseDate"] = card_release_dates

    ## Remove the list from types and fill in the first type
    types = []
    for type_ in cards_df.types:
        try:
            types.append(type_[0])
        except:
            types.append(type_)
    cards_df.types = pd.Series(types)

    ## Clean up weaknesses
    weaknesses = []
    for weakness in cards_df.weaknesses:
        try:
            weaknesses.append(weakness[0]["type"])
        except:
            types.append(weakness)

    cards_df.weaknesses = pd.Series(weaknesses)

    ## Clean up resistances

    resistances = []
    for resistance in cards_df.resistances:
        try:
            resistances.append(resistance[0]["type"])
        except:
            resistances.append(resistance)

    cards_df["resistances"] = pd.Series(resistances)

    return cards_df
