import pickle
from os import path
import pandas as pd

three_dirs_up = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


def get_attacks():
    """Load linked pickle wich return dict with all attacks"""

    pickles_path = path.join(
        three_dirs_up, "raw_data/scrapping_nicolas/learnset_dictionary.pkl"
    )

    return pickle.load(open(pickles_path, "rb"))


def get_lore():
    """Load linked pickle wich return dict with all attacks"""

    pickles_path = path.join(
        three_dirs_up, "raw_data/scrapping_nicolas/corpus_lore.pkl"
    )

    return pickle.load(open(pickles_path, "rb"))


def get_stats():
    """Load linked pickle wich return dict with all attacks"""

    pickles_path = path.join(
        three_dirs_up, "raw_data/scrapping_nicolas/df_stats_lxml.pkl"
    )

    return pd.read_pickle(pickles_path)
