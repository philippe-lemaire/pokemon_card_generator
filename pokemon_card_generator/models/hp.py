from pokemon_card_generator.data.pokemon_list import pokemon_list


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
