from pokemon_card_generator.data.pokemon_list import pokemon_list
from pokemon_card_generator.data.card_data import get_card_data
from pokemon_card_generator.data.base_card_dict import base_card_dict

cards_df = get_card_data()


def predict_hp(pokémon_name, *args, **kwargs):
    """Dummy baseline: A Pokémon's HP"""
    # load the cards_df
    # cards_df = get_card_data()
    global cards_df
    local_df = cards_df.copy()
    time_series_df = local_df[["name", "releaseDate", "hp"]]

    # one observation per pokemon in our list
    observations = []

    for pokemon in pokemon_list:
        mask = time_series_df["name"] == pokemon
        df = time_series_df[mask]
        observations.append(df.hp.to_list())

    hp = observations[pokemon_list.index(pokémon_name)][-1]
    return str(int(hp))


def predict_evolvesFrom(pokémon_name, *args, **kwargs):
    """Dummy baseline: checks last card and returns its evolves from"""
    # load the cards_df
    # cards_df = get_card_data()
    global cards_df
    local_df = cards_df.copy()

    time_series_df = local_df[["name", "releaseDate", "evolvesFrom"]]

    # one observation per pokemon in our list
    observations = []

    for pokemon in pokemon_list:
        mask = time_series_df["name"] == pokemon
        df = time_series_df[mask]
        observations.append(df.evolvesFrom.to_list())

    evolvesFrom = observations[pokemon_list.index(pokémon_name)][0]
    if isinstance(evolvesFrom, float):
        evolvesFrom = ""

    return evolvesFrom


def create_card(pokémon_name, rarity):
    card_dict = base_card_dict.copy()
    card_dict["data"]["hp"] = predict_hp(pokémon_name)
    card_dict["data"]["name"] = pokémon_name
    card_dict["data"]["rarity"] = rarity
    card_dict["data"]["evolvesFrom"] = predict_evolvesFrom(pokémon_name)
    return card_dict
