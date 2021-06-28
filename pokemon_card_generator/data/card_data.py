import csv
import pandas as pd


def get_card_data():
    """Concatenates all the pickles in 'raw_data/pickles' and returns a dataframe.
    Usage: from pokemon_card_generator.data import card_data; card_df = card_data.get_card_data()"""
    # list all the files in data
    from os import walk, path

    pickles_path = "../raw_data/pickles"
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

    return cards_df
