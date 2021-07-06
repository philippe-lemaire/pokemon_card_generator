from pokemon_card_generator.data.pokemon_list import pokemon_list


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
