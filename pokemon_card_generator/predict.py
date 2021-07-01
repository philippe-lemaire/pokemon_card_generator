from pokemon_card_generator.data.pokemon_list import pokemon_list
from pokemon_card_generator.data.card_data import get_card_data
from pokemon_card_generator.data.base_card_dict import base_card_dict
from pokemon_card_generator.models.attacks import *
from pokemon_card_generator.data.scrap_data import get_stats
from pokemon_card_generator.models.flavor_text import generate_flavor


def predict_hp(pokémon_name, cards_df, *args, **kwargs):
    """Dummy baseline: A Pokémon's HP is the HP of its most recent card."""

    time_series_df = cards_df[["name", "releaseDate", "hp"]]

    # one observation per pokemon in our list
    observations = []

    for pokemon in pokemon_list:
        mask = time_series_df["name"] == pokemon
        df = time_series_df[mask]
        observations.append(df.hp.to_list())

    hp = observations[pokemon_list.index(pokémon_name)][-1]
    return str(int(hp))


def predict_evolvesFrom(pokémon_name, cards_df, *args, **kwargs):
    """Dummy baseline, returns the first card with the same name's evolves from."""

    time_series_df = cards_df[["name", "releaseDate", "evolvesFrom"]]

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


def predict_types(pokémon_name, cards_df, *args, **kwargs):
    """Dummy baseline, returns the same type as the last card of the same name."""

    time_series_df = cards_df[["name", "releaseDate", "types"]]

    # one observation per pokemon in our list
    observations = []

    for pokemon in pokemon_list:
        mask = time_series_df["name"] == pokemon
        df = time_series_df[mask]
        observations.append(df.types.to_list())

    types = observations[pokemon_list.index(pokémon_name)][-1]

    return [types]


def predict_weaknesses(pokémon_name, cards_df, *args, **kwargs):
    """Dummy baseline, returns the same type as the last card of the same name."""

    time_series_df = cards_df[["name", "releaseDate", "weaknesses"]]

    # one observation per pokemon in our list
    observations = []

    for pokemon in pokemon_list:
        mask = time_series_df["name"] == pokemon
        df = time_series_df[mask]
        observations.append(df.weaknesses.to_list())

    weakness_type = observations[pokemon_list.index(pokémon_name)][0]

    weaknesses = [{"type": weakness_type, "value": "x2"}]
    if weaknesses[0]["type"] == "No_weaknesses":
        weaknesses = []
    return weaknesses


def predict_resistances(pokémon_name, cards_df, *args, **kwargs):
    """Dummy baseline, returns the same resistances the last card of the same name."""

    time_series_df = cards_df[["name", "releaseDate", "resistances"]]

    # one observation per pokemon in our list
    observations = []

    for pokemon in pokemon_list:
        mask = time_series_df["name"] == pokemon
        df = time_series_df[mask]
        observations.append(df.resistances.to_list())

    resistance_type = observations[pokemon_list.index(pokémon_name)][0]

    resistances = [{"type": resistance_type, "value": "x2"}]
    if resistances[0]["type"] == "No_resistances":
        resistances = []
    return resistances


def predict_weight(pokémon_name, cards_df, *args, **kwargs):
    base_stats = get_stats()
    weight = base_stats.Weight[pokemon_list.index(pokémon_name)]
    return weight


def predict_retreatCost(pokémon_name, cards_df, *args, **kwargs):
    """Dummy baseline, returns a predict cost based on weight"""
    base_stats = get_stats()
    weight = base_stats.Weight[pokemon_list.index(pokémon_name)]
    # remove " lbs" from weight
    num_weight = float(weight[:-4])
    if num_weight <= 2:
        return []
    if num_weight <= 100:
        return ["Colorless"]
    if num_weight <= 400:
        return ["Colorless"] * 2
    return ["Colorless"] * 3


def create_card(pokémon_name, rarity):
    """Takes a pokémon name and rarity level and generates a card. Returns a dict"""
    cards_df = get_card_data()

    card_dict = base_card_dict.copy()
    card_dict["data"]["hp"] = predict_hp(pokémon_name, cards_df)
    card_dict["data"]["name"] = pokémon_name
    card_dict["data"]["rarity"] = rarity
    card_dict["data"]["evolvesFrom"] = predict_evolvesFrom(pokémon_name, cards_df)
    card_dict["data"]["types"] = predict_types(pokémon_name, cards_df)
    card_dict["data"]["attacks"] = attacks_generator(pokémon_name, cards_df, rarity)
    card_dict["data"]["weaknesses"] = predict_weaknesses(pokémon_name, cards_df, rarity)
    card_dict["data"]["resistances"] = predict_resistances(
        pokémon_name, cards_df, rarity
    )
    card_dict["data"]["weight"] = predict_weight(pokémon_name, cards_df)
    card_dict["data"]["retreatCost"] = predict_retreatCost(pokémon_name, cards_df)
    card_dict["data"]["flavorText"] = generate_flavor(pokémon_name)
    return card_dict
