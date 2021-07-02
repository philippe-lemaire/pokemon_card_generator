import csv
import pandas as pd
from pokemon_card_generator.data.set_data import get_sets
from os import walk, path
import string


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

    # drop one card with japanese text
    cards_df = cards_df.drop(cards_df[cards_df.id == "xy12-109"].index)

    # drop cards of squads (several pokémon on the same card)
    cards_df = cards_df.drop(cards_df[cards_df.name.str.contains("&")].index)

    ## remove useless columns
    useless_cols = [
        "level",
        "number",
        "ancientTrait",
        "artist",
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
        len(cost) if isinstance(cost, list) else cost for cost in attack2_cost
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
        len(cost) if isinstance(cost, list) else cost for cost in attack3_cost
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

    # remove light from name
    cards_df.name = cards_df.name.apply(lambda x: x.replace("Light ", ""))

    # remove dark from name
    cards_df.name = cards_df.name.apply(lambda x: x.replace("Dark ", ""))

    # remove trainer's names from pokemon name
    trainer_names = [
        "Blaine's ",
        "Brock's ",
        "Erika's ",
        "Lt. Surge's ",
        "Misty's ",
        "Rocket's ",
        "Sabrina's ",
        "Giovanni's ",
        "Koga's ",
        "_____'s ",
        "Flying ",
        "Surfing ",
        "Shining ",
        "Ash's ",
        "Team Magma's ",
        "Team Aqua's ",
        "Holon's ",
        "Imakuni?'s ",
        "Ash-",
    ]

    for trainer in trainer_names:
        cards_df.name = cards_df.name.apply(lambda x: x.replace(trainer, ""))

    # remove [A] and so on from Unown's names

    letters = [f" [{letter}]" for letter in string.ascii_uppercase]

    for letter in letters:
        cards_df.name = cards_df.name.apply(lambda x: x.replace(letter, ""))

    # fill nan in weaknesess
    cards_df.weaknesses.fillna("No_weaknesses", inplace=True)

    # fill nan in resistances
    cards_df.resistances.fillna("No_resistances", inplace=True)

    # fill nan in evolves to

    cards_df.evolvesTo.fillna("final_stage", inplace=True)

    ## create V_pokemon column and remove " V" from end of name
    V_pokemon = [1 if name.endswith(" V") else 0 for name in cards_df.name]
    cards_df["V_pokemon"] = V_pokemon
    # remove " V" from name
    cards_df.name = cards_df.name.apply(lambda x: x.rstrip(" V"))

    ## create Vmax_pokemon column and remove " VMAX" at the end of name
    Vmax_pokemon = [1 if name.endswith(" VMAX") else 0 for name in cards_df.name]
    cards_df["Vmax_pokemon"] = Vmax_pokemon
    # remove " VMAX" from name
    cards_df.name = cards_df.name.apply(lambda x: x.rstrip(" VMAX"))

    # remove " -G" from name
    cards_df.name = cards_df.name.apply(lambda x: x.rstrip("-G"))
    # remove " -E" from name
    cards_df.name = cards_df.name.apply(lambda x: x.rstrip("-E"))
    cards_df.name = cards_df.name.apply(lambda x: x.rstrip(" E"))

    # remove "M " at the begining of Mega evolution cards
    cards_df.name = cards_df.name.apply(lambda x: x.replace("M ", ""))

    # remove "Rapid Strike" and "Single Strike" from name
    gimmicks = [
        "Rapid Strike ",
        "Single Strike ",
        " δ",
        " ◇",
        " LV.",
        " East Sea",
        " West Sea",
        " Plant Cloak",
        " Sandy Cloak",
        " Trash Cloak",
        " E4",
        " GL",
        " FB",
        "Galarian ",
        "Alolan ",
        "Dawn Wings ",
        "Dusk Wings ",
        "Dawn Wings ",
        "Primal ",
        " BREAK",
        "Black ",
        "White ",
        " LEGEND",
        " Star",
        "Detective ",
        "Armored ",
        "Special Delivery ",
        "Dusk Mane ",
        "Ultra ",
        # rotom is fun
        "Mow ",
        "Heat ",
        "Wash ",
        "Frost ",
        # forme
        " Speed Forme",
        " Normal Forme",
        " Rain Form",
        " Attack Forme",
        " Defense Forme",
        " Snow-Cloud Form",
        " Sunny Form",
        "Snow-cloud ",
        "Sunny ",
        "Rain ",
    ]

    for gimmick in gimmicks:
        cards_df.name = cards_df.name.apply(lambda x: x.replace(gimmick, ""))

    ## clean up nidoran male and female names
    cards_df.name = cards_df.name.apply(lambda x: x.replace("Nidoran ", "Nidoran"))

    ## clean up " ex"
    def clean_ex(s):
        if s.endswith(" ex"):
            s = s[:-3]
        return s

    cards_df.name = cards_df.name.apply(lambda x: clean_ex(x))

    ## clean up trailing letter
    def clean_trailing(s):
        for letter in string.ascii_uppercase + "?" + "!":
            if s.endswith(f" {letter}"):
                s = s[:-2]
        return s

    cards_df.name = cards_df.name.apply(lambda x: clean_trailing(x))

    return cards_df
