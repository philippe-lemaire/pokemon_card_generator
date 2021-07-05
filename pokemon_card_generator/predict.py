import pokemon_card_generator
from pokemon_card_generator.data.pokemon_list import pokemon_list
from pokemon_card_generator.data.card_data import get_card_data
from pokemon_card_generator.data.base_card_dict import base_card_dict
from pokemon_card_generator.models.attacks import *
from pokemon_card_generator.models.abilities import *
from pokemon_card_generator.models.hp import predict_hp
from pokemon_card_generator.models.type import predict_types
from pokemon_card_generator.models.evolves_from import predict_evolvesFrom
from pokemon_card_generator.models.resistances import predict_resistances
from pokemon_card_generator.models.weaknesses import predict_weaknesses
from pokemon_card_generator.models.retreat_cost import predict_retreatCost
from pokemon_card_generator.data.scrap_data import get_stats
from pokemon_card_generator.models.flavor_text import generate_flavor
from pokemon_card_generator.models.get_illustration import get_illustration


def get_weight_and_height_and_cat(pokémon_name, cards_df, *args, **kwargs):
    base_stats = get_stats()
    weight = base_stats.Weight[pokemon_list.index(pokémon_name)]
    height = base_stats.Height[pokemon_list.index(pokémon_name)]
    cat = base_stats.Category[pokemon_list.index(pokémon_name)] + " Pokémon"
    return weight, height, cat


def get_num(pokémon_name, cards_df, *args, **kwargs):
    """reads the national Pokedex number from df_cards"""
    return cards_df[cards_df.name == pokémon_name].nationalPokedexNumbers.to_list()[0]


def create_card(pokémon_name, rarity):
    """Takes a pokémon name and rarity level and generates a card. Returns a dict"""
    cards_df = get_card_data()

    card_dict = base_card_dict.copy()
    card_dict["data"]["hp"] = predict_hp(pokémon_name, cards_df)
    card_dict["data"]["name"] = pokémon_name
    card_dict["data"]["rarity"] = rarity
    card_dict["data"]["evolvesFrom"] = predict_evolvesFrom(pokémon_name, cards_df)
    card_dict["data"]["types"] = predict_types(pokémon_name, cards_df)
    card_dict["data"]["abilities"], ability_presence = abilitys_generator(
        pokémon_name, cards_df, rarity
    )
    card_dict["data"]["attacks"] = attacks_generator(
        pokémon_name, cards_df, rarity, ability_presence
    )

    card_dict["data"]["weaknesses"] = predict_weaknesses(pokémon_name, cards_df, rarity)
    card_dict["data"]["resistances"] = predict_resistances(
        pokémon_name, cards_df, rarity
    )

    card_dict["data"]["retreatCost"] = predict_retreatCost(pokémon_name, cards_df)
    card_dict["data"]["flavorText"] = generate_flavor(pokémon_name)

    # get weight, height, pokedex number and family
    weight, height, cat = get_weight_and_height_and_cat(pokémon_name, cards_df)
    card_dict["data"]["weight"] = weight
    card_dict["data"]["height"] = height
    card_dict["data"]["category"] = cat
    card_dict["data"]["nationalPokedexNumbers"] = get_num(pokémon_name, cards_df)
    card_dict["data"]["illustration"] = get_illustration(pokémon_name, cards_df)

    return card_dict
