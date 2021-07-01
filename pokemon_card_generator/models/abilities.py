from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
import random


def df_abilitys_creation(cards_df):
    cards_df_abilitys = cards_df.copy()
    cards_df_abilitys = cards_df_abilitys[
        ["name", "rarity", "ability1_name", "ability1_text"]
    ]
    # Data engineering ab 1 !
    cards_df_abilitys["ability1_existence"] = [
        1 if len(item) > 0 else 0 for item in cards_df_abilitys["ability1_name"]
    ]

    return cards_df_abilitys


def clean_rarity(cards_df_abilitys):
    keys = cards_df_abilitys["rarity"].unique().tolist()
    list_values = [5, 4, 2, 1, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    rry_dict = {k: v for k, v in zip(keys, list_values)}
    cards_df_abilitys["rarity"] = cards_df_abilitys["rarity"].map(rry_dict)
    return cards_df_abilitys


def abilitys_prediction(cards_df_abilitys, rarity):
    """r"""
    # Filtre par Nom du pokemon
    # cards_df_abilitys = cards_df_abilitys[cards_df_abilitys.name == pokémon_name]

    # Filtre de la rareté
    # cards_df_abilitys = cards_df_abilitys.drop(cards_df_abilitys[cards_df_abilitys.rarity != rarity].index)

    # Preparation du dataframe pour la lgst reg
    lgst_reg_cards_df_abilitys = cards_df_abilitys[["rarity", "ability1_existence"]]
    # Ready X and y
    data = lgst_reg_cards_df_abilitys.copy()
    X = data.drop(columns=["ability1_existence"])
    y = data["ability1_existence"]
    # Split into Train/Test 70% / 30%
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    # Data Scaling
    m_scaler = MinMaxScaler()
    m_scaler.fit_transform(X_train)
    m_scaler.transform(X_test)
    # Model training
    model = LogisticRegression(solver="lbfgs", max_iter=500)
    model = model.fit(X_train, y_train)
    result_proba = model.predict_proba([[rarity]])

    return result_proba[0][1]


def abilitys_generator(pokémon_name, cards_df, rarity):
    """ """
    dtn1 = {"ability1_name": "name", "ability1_text": "text"}
    result = []

    cards_df_abilitys = df_abilitys_creation(cards_df)
    cards_df_abilitys = clean_rarity(cards_df_abilitys)

    proba = abilitys_prediction(cards_df_abilitys, rarity) * 100
    proba_rng = random.randint(0, 90)

    if proba_rng <= round(proba):
        df_abilitys = cards_df_abilitys[["ability1_name", "ability1_text"]]
        df_abilitys.replace("", inplace=True)
        df_abilitys.dropna(subset=["ability1_name"])
        df_abilitys = df_abilitys.rename(dtn1, axis=1)

        df_abilitys = df_abilitys.drop_duplicates()

        size = len(df_abilitys)
        rng = random.randint(0, size)

        df_abilitys = df_abilitys.iloc[rng - 1, :]
        result.append(df_abilitys.to_dict())
        return result
    else:
        return result
