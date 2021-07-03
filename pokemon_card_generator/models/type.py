from pokemon_card_generator.data.pokemon_list import pokemon_list


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
