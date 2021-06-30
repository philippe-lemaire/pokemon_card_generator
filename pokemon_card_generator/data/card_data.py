import csv
import pandas as pd
from pokemon_card_generator.data.set_data import get_sets
from os import walk, path


def get_card_data():
    """Concatenates all the pickles in 'raw_data/pickles' and returns a dataframe.
    Usage: from pokemon_card_generator.data import card_data; card_df = card_data.get_card_data()"""
    # list all the files in data

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

    ## Clean up subtypes

    subtypes = []
    for subtype in cards_df.subtypes:
        try:
            subtypes.append(subtype[0])
        except:
            subtypes.append(subtype)

    cards_df["subtypes"] = pd.Series(subtypes)

    ## set hp column to numbers
    hp_list = []
    for card_hp in cards_df.hp:
        try:
            hp_list.append(int(card_hp))
        except:
            hp_list.append(card_hp)

    cards_df["hp"] = pd.Series(hp_list)

    ## remove non pokémon cards

    cards_df = cards_df[cards_df.supertype == "Pokémon"]

    ## remove useless columns
    useless_cols = [
        "level",
        "number",
        "ancientTrait",
        "artist",
        "nationalPokedexNumbers",
        "legalities",
        "images",
        "tcgplayer",
        "index",
        "supertype",
        "set",
        "retreatCost",
    ]

    cards_df.drop(columns=useless_cols, inplace=True)

    ## flatten attack 1
    attack1_name = [
        item[0]["name"] if isinstance(item, list) else item for item in cards_df.attacks
    ]

    attack1_cost = [
        item[0]["cost"] if isinstance(item, list) else item for item in cards_df.attacks
    ]

    attack1_converted_cost = [
        len(cost) if isinstance(cost, list) else cost for cost in attack1_cost
    ]

    attack1_damage = [
        item[0]["damage"] if isinstance(item, list) else item
        for item in cards_df.attacks
    ]

    attack1_text = [
        item[0]["text"] if isinstance(item, list) else item for item in cards_df.attacks
    ]

    cards_df["attack1_name"] = attack1_name
    cards_df["attack1_cost"] = attack1_cost
    cards_df["attack1_converted_cost"] = attack1_converted_cost
    cards_df["attack1_damage"] = attack1_damage
    cards_df["attack1_text"] = attack1_text

    ## flatening attack 2
    attack2_name = [
        item[1]["name"] if isinstance(item, list) and len(item) > 1 else ""
        for item in cards_df.attacks
    ]

    attack2_cost = [
        item[1]["cost"] if isinstance(item, list) and len(item) > 1 else ""
        for item in cards_df.attacks
    ]

    attack2_converted_cost = [
        len(cost) if isinstance(cost, list) and len(cost) > 1 else cost
        for cost in attack2_cost
    ]

    attack2_damage = [
        item[1]["damage"] if isinstance(item, list) and len(item) > 1 else ""
        for item in cards_df.attacks
    ]

    attack2_text = [
        item[1]["text"] if isinstance(item, list) and len(item) > 1 else ""
        for item in cards_df.attacks
    ]

    cards_df["attack2_name"] = attack2_name
    cards_df["attack2_cost"] = attack2_cost
    cards_df["attack2_converted_cost"] = attack2_converted_cost
    cards_df["attack2_damage"] = attack2_damage
    cards_df["attack2_text"] = attack2_text

    ## flatten attack 3
    attack3_name = [
        item[2]["name"] if isinstance(item, list) and len(item) > 2 else ""
        for item in cards_df.attacks
    ]

    attack3_cost = [
        item[2]["cost"] if isinstance(item, list) and len(item) > 2 else ""
        for item in cards_df.attacks
    ]

    attack3_converted_cost = [
        len(cost) if isinstance(cost, list) and len(cost) > 1 else cost
        for cost in attack3_cost
    ]

    attack3_damage = [
        item[2]["damage"] if isinstance(item, list) and len(item) > 2 else ""
        for item in cards_df.attacks
    ]

    attack3_text = [
        item[2]["text"] if isinstance(item, list) and len(item) > 2 else ""
        for item in cards_df.attacks
    ]

    cards_df["attack3_name"] = attack3_name
    cards_df["attack3_cost"] = attack3_cost
    cards_df["attack3_converted_cost"] = attack3_converted_cost
    cards_df["attack3_damage"] = attack3_damage
    cards_df["attack3_text"] = attack3_text

    ## drop column attacks

    cards_df.drop(columns=["attacks"], inplace=True)

    ability1_name = [
        item[0]["name"] if isinstance(item, list) else "" for item in cards_df.abilities
    ]

    # flatten ability 1
    ability1_text = [
        item[0]["text"] if isinstance(item, list) else "" for item in cards_df.abilities
    ]

    cards_df["ability1_name"] = ability1_name
    cards_df["ability1_text"] = ability1_text

    ## flatten abitily 2
    ability2_name = [
        item[1]["name"] if isinstance(item, list) and len(item) > 1 else ""
        for item in cards_df.abilities
    ]

    ability2_text = [
        item[1]["text"] if isinstance(item, list) and len(item) > 1 else ""
        for item in cards_df.abilities
    ]

    cards_df["ability2_name"] = ability2_name
    cards_df["ability2_text"] = ability2_text

    # drop column abilities
    cards_df.drop(columns=["abilities"], inplace=True)

    # drop cards with no rarity
    cards_df = cards_df.drop(cards_df[cards_df.rarity.isna()].index)

    return cards_df
