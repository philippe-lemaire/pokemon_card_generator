from pokemon_card_generator.data.pokemon_list import pokemon_list
from pokemon_card_generator.data.scrap_data import get_stats


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
