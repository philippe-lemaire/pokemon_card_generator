from pokemon_card_generator.data.pokemon_list import pokemon_list


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
