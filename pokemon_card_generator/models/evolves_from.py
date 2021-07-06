from pokemon_card_generator.data.pokemon_list import pokemon_list


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
