from pokemon_card_generator.data.pokemon_list import pokemon_list
from sklearn.linear_model import LinearRegression
import numpy as np


def predict_hp(pokémon_name, rarity, cards_df):
    "returns a linear regression of HP for a given pokémon_name"
    pokemon_hp_df = cards_df[cards_df.name == pokémon_name].reset_index()
    features = [
        #  'subtypes',
        #   'hp',
        #  'evolvesFrom',
        "rarity",
        # 'evolvesTo',
        #  'V_pokemon',
        # 'Vmax_pokemon'
    ]

    # encode rarity
    keys = cards_df["rarity"].unique().tolist()
    list_values = [5, 4, 2, 1, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    rry_dict = {k: v for k, v in zip(keys, list_values)}
    pokemon_hp_df["rarity"] = pokemon_hp_df["rarity"].map(rry_dict)
    y = pokemon_hp_df.pop("hp")
    X = pokemon_hp_df[features]
    model = LinearRegression()
    model.fit(X, y)

    rarity = np.array(rarity)
    rarity = rarity.reshape(1, -1)
    prediction = model.predict(rarity)[0]
    # round to the nearest 10
    result = round(prediction / 10) * 10
    return result
