import random


def df_atk_creation(cards_df):
    df_atk = cards_df.copy()
    df_atk = df_atk[
        [
            "name",
            "rarity",
            "attack1_name",
            "attack1_cost",
            "attack1_damage",
            "attack1_text",
            "attack2_name",
            "attack2_cost",
            "attack2_damage",
            "attack2_text",
            "attack3_name",
            "attack3_cost",
            "attack3_damage",
            "attack3_text",
        ]
    ]
    return df_atk


def clean_rarity(df_atk):
    keys = df_atk["rarity"].unique().tolist()
    list_values = [5, 4, 2, 1, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    rry_dict = {k: v for k, v in zip(keys, list_values)}
    df_atk["rarity"] = df_atk["rarity"].map(rry_dict)
    return df_atk


def clean_damage(df_atk):
    df_atk["attack1_damage"] = df_atk["attack1_damage"].fillna(0)
    df_atk["attack2_damage"] = df_atk["attack2_damage"].fillna(0)
    df_atk["attack3_damage"] = df_atk["attack3_damage"].fillna(0)
    return df_atk


def atk_prediction(pokémon_name, cards_df, rarity):
    cards_df = cards_df[cards_df.name == pokémon_name]
    cards_df = cards_df.drop(cards_df[cards_df.rarity != rarity].index)
    if len(cards_df) == 0:
        err = print(" Rarity does not exist ! ")
        return err
    else:
        size = len(cards_df)
        rng = random.randint(0, size)
        df_atk = cards_df.iloc[rng - 1, :]
        df_atk = df_atk.drop(["name", "rarity"])
        return df_atk


def attacks_generator(pokémon_name, cards_df, rarity, ability_presence):
    """Predict attacks dammage according name and rarity"""

    dtn1 = {
        "attack1_name": "name",
        "attack1_cost": "cost",
        "attack1_damage": "damage",
        "attack1_text": "text",
    }
    dtn2 = {
        "attack2_name": "name",
        "attack2_cost": "cost",
        "attack2_damage": "damage",
        "attack2_text": "text",
    }
    dtn3 = {
        "attack3_name": "name",
        "attack3_cost": "cost",
        "attack3_damage": "damage",
        "attack3_text": "text",
    }

    df_atk = df_atk_creation(cards_df)
    df_atk = clean_rarity(cards_df)
    df_atk = clean_damage(cards_df)
    df_atk = atk_prediction(pokémon_name, cards_df, rarity)
    df_atk_1 = df_atk[
        ["attack1_name", "attack1_cost", "attack1_damage", "attack1_text"]
    ]
    df_atk_1 = df_atk_1.rename(dtn1, axis="index")
    df_atk_2 = df_atk[
        ["attack2_name", "attack2_cost", "attack2_damage", "attack2_text"]
    ]
    df_atk_2 = df_atk_2.rename(dtn2, axis="index")
    df_atk_3 = df_atk[
        ["attack3_name", "attack3_cost", "attack3_damage", "attack3_text"]
    ]
    df_atk_3 = df_atk_3.rename(dtn3, axis="index")
    # use 2 attacks at most
    liste_of_df_atk = [df_atk_1, df_atk_2]
    # if there is no ability, then we can add a third attack, if any
    if not ability_presence:
        liste_of_df_atk.append(df_atk_3)
    result = [item.to_dict() for item in liste_of_df_atk if item["name"] != ""]
    return result
