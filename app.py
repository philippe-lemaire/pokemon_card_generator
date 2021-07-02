import streamlit as st
import requests
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from pokemon_card_generator.data.pokemon_list import pokemon_list
from matplotlib.offsetbox import OffsetImage, AnchoredOffsetbox

# import json
# import numpy as np

# streamlit web
st.markdown(
    "<h1 style='text-align: center; color: blue;'>Pokémon Card Generator</h1>",
    unsafe_allow_html=True,
)

# web inputs from stremlit
# Using the "with" syntax
with st.form(key="my_form"):
    st.markdown(
        "<p style='text-align: center; color: black;'>Pokémon name</p>",
        unsafe_allow_html=True,
    )
    pokemon_selected = st.selectbox("", (pokemon_list))
    rarity = ["common", "uncommon", "promo", "rare", "shiny"]
    rarity_selected = st.radio("Rarity", rarity)
    submit_button = st.form_submit_button(label="Generate")

# horizontal radio buttons
st.write(
    "<style>div.row-widget.stRadio > div{flex-direction:row;}</style>",
    unsafe_allow_html=True,
)

# return rarity number
if rarity_selected == "common":
    rarity_selected = 1
if rarity_selected == "uncommon":
    rarity_selected = 2
if rarity_selected == "promo":
    rarity_selected = 3
if rarity_selected == "rare":
    rarity_selected = 4
if rarity_selected == "shiny":
    rarity_selected = 5

# address of the api prediction
url = "https://api.pokemontcg.io/v2/cards/swsh4-57"
url2 = "https://api.pokemontcg.io/v2/cards/xy6-75"
url_api = "https://pokecardgenerator-tybpdn52ha-ew.a.run.app/create_card?pok%C3%A9mon_name=Pikachu&rarity=2"
api = "https://pokecardgenerator-tybpdn52ha-ew.a.run.app/create_card"

# get prediction
params = dict(pokémon_name=pokemon_selected, rarity=rarity_selected)
response = requests.get(url_api, params=params)
prediction = response.json()

# input from prediction
pokemon_type = prediction["data"]["types"][0].lower()
pokemon_name = prediction["data"]["name"]
hp = prediction["data"]["hp"]
nationalPokedexNumbers = prediction["data"]["nationalPokedexNumbers"][0]

# category
if prediction["data"].get("category"):
    pokemon_category = prediction["data"]["category"]
else:
    pokemon_category = "Pokémon"

# height
if prediction["data"].get("height"):
    pokemon_height = prediction["data"]["height"]
else:
    pokemon_height = "5'"

# weight
if prediction["data"].get("weight"):
    pokemon_weight = prediction["data"]["weight"]
else:
    pokemon_weight = "12.4 lbs"

# ability
if prediction["data"].get("abilities"):
    ability_name = prediction["data"]["abilities"][0]["name"]
    ability_text = prediction["data"]["abilities"][0]["text"]

# attacks
if len(prediction["data"]["attacks"]) > 0:
    pokemon_attack1_cost = prediction["data"]["attacks"][0]["cost"]
    pokemon_attack1_name = prediction["data"]["attacks"][0]["name"]
    pokemon_attack1_damage = prediction["data"]["attacks"][0]["damage"]
    pokemon_attack1_text = prediction["data"]["attacks"][0]["text"]
if len(prediction["data"]["attacks"]) > 1:
    pokemon_attack2_cost = prediction["data"]["attacks"][1]["cost"]
    pokemon_attack2_name = prediction["data"]["attacks"][1]["name"]
    pokemon_attack2_damage = prediction["data"]["attacks"][1]["damage"]
    pokemon_attack2_text = prediction["data"]["attacks"][1]["text"]

# weakness
if prediction["data"].get("weaknesses"):
    pokemon_weakness_type = prediction["data"]["weaknesses"][0]["type"]
    pokemon_weakness_value = prediction["data"]["weaknesses"][0]["value"]

# resistance
if prediction["data"].get("resistances"):
    pokemon_resistance_type = prediction["data"]["resistances"][0]["type"]
    pokemon_resistance_value = prediction["data"]["resistances"][0]["value"]

# retreat
if prediction["data"].get("retreatCost"):
    pokemon_retreat_cost = prediction["data"]["retreatCost"][0]

# flavor text
if prediction["data"].get("flavorText"):
    pokemon_flavor_text = prediction["data"]["flavorText"]

# text positionning
position_x1 = 30
position_x2 = position_x1 + 20
position_x3 = position_x2 + 77
position_x4 = position_x3 + 83
position_x5 = position_x4 + 110
position_x6 = position_x5 + 220
position_x7 = position_x6 + 30
position_x8 = position_x7 + 50
position_y1 = 570
position_y2 = position_y1 + 60
position_y3 = position_y2 + 60
position_y4 = position_y3 + 60
position_y5 = position_y4 + 60
position_y6 = position_y5 + 60
position_y7 = position_y6 + 71
position_y8 = position_y7 + 30

# define paths
main_path = "pokemon_card_generator/frontend/images/"
set_path = main_path + "cleaned_cards"
ability_img_path = main_path + "card_icons/ability.png"
image_full_path = os.path.join(set_path, pokemon_type + ".png")


# def remove_border(image):
#     image_read = mpimg.imread(image)
#     sizes = np.shape(image_read)
#     fig = plt.figure()
#     fig.set_size_inches(1.0 * sizes[0] / sizes[1], 1, forward=False)
#     ax = plt.Axes(fig, [0.0, 0.0, 1.0, 1.0])
#     ax.set_axis_off()
#     fig.add_axes(ax)
#     ax.imshow(image_read)
#     plt.savefig("cache_image.png", dpi=sizes[0], cmap="hot")
#     plt.show()


# print main image
def show_image():
    fig = plt.figure(frameon=True, figsize=(9, 12), dpi=100.0)
    plt.axis("off")  # remove axis
    ax1 = plt.imshow(mpimg.imread(image_full_path), alpha=0.7)  # background card
    plt.text(position_x3, 75, pokemon_name, fontsize=25, color="black")  # name
    plt.text(position_x6, 75, "HP", fontsize=13, color="black")  # HP (1)
    plt.text(position_x7, 75, hp, fontsize=25, color="black")  # HP (2)
    plt.text(
        367,
        506,
        "NO. "
        + str(nationalPokedexNumbers)
        + "  "
        + pokemon_category
        + "  HT: "
        + pokemon_height
        + "  WT: "
        + pokemon_weight,
        ha="center",
        fontsize=12,
        color="black",
    )  # nationalPokedexNumbers + category + height + weight
    if prediction["data"].get("abilities"):
        plt.text(
            position_x4, position_y1, ability_name, fontsize=22, color="black"
        )  # ability name
        plt.text(
            position_x2,
            position_y2,
            ability_text,
            ha="left",
            fontsize=16,
            color="black",
            wrap=True,
        )  # ability text
        if len(prediction["data"]["attacks"]) > 0:
            plt.text(
                position_x2,
                position_y3,
                pokemon_attack1_cost,
                fontsize=8,
                color="black",
            )  # attack cost
            plt.text(
                position_x4,
                position_y3,
                pokemon_attack1_name,
                fontsize=22,
                color="black",
            )  # attack name
            plt.text(
                position_x8,
                position_y3,
                pokemon_attack1_damage,
                fontsize=22,
                color="black",
            )  # attack damage
            plt.text(
                position_x2,
                position_y4,
                pokemon_attack1_text,
                fontsize=16,
                color="black",
                wrap=True,
            )  # attack text
        if len(prediction["data"]["attacks"]) > 1:
            plt.text(
                position_x2,
                position_y5,
                pokemon_attack2_cost,
                fontsize=8,
                color="black",
            )  # attack cost
            plt.text(
                position_x4,
                position_y5,
                pokemon_attack2_name,
                fontsize=22,
                color="black",
            )  # attack name
            plt.text(
                position_x8,
                position_y5,
                pokemon_attack2_damage,
                fontsize=22,
                color="black",
            )  # attack damage
            plt.text(
                position_x2,
                position_y6,
                pokemon_attack2_text,
                fontsize=16,
                color="black",
                wrap=True,
            )  # attack text
    else:
        if len(prediction["data"]["attacks"]) > 0:
            plt.text(
                position_x2,
                position_y1,
                pokemon_attack1_cost,
                fontsize=8,
                color="black",
            )  # attack cost
            plt.text(
                position_x4,
                position_y1,
                pokemon_attack1_name,
                fontsize=22,
                color="black",
            )  # attack name
            plt.text(
                position_x8,
                position_y1,
                pokemon_attack1_damage,
                fontsize=22,
                color="black",
            )  # attack damage
            plt.text(
                position_x2,
                position_y2,
                pokemon_attack1_text,
                fontsize=16,
                color="black",
                wrap=True,
            )  # attack text
        if len(prediction["data"]["attacks"]) > 1:
            plt.text(
                position_x2,
                position_y3,
                pokemon_attack2_cost,
                fontsize=8,
                color="black",
            )  # attack cost
            plt.text(
                position_x4,
                position_y3,
                pokemon_attack2_name,
                fontsize=22,
                color="black",
            )  # attack name
            plt.text(
                position_x8,
                position_y3,
                pokemon_attack2_damage,
                fontsize=22,
                color="black",
            )  # attack damage
            plt.text(
                position_x2,
                position_y4,
                pokemon_attack2_text,
                fontsize=16,
                color="black",
                wrap=True,
            )  # attack text
    if prediction["data"].get("weaknesses"):
        plt.text(
            position_x3, position_y6, pokemon_weakness_type, fontsize=8, color="black"
        )  # weakness type
        plt.text(
            position_x3 + 20,
            position_y6,
            pokemon_weakness_value,
            fontsize=20,
            color="black",
        )  # weakness value
    if prediction["data"].get("resistances"):
        plt.text(
            position_x5, position_y6, pokemon_resistance_type, fontsize=8, color="black"
        )  # resistance type
        plt.text(
            position_x5 + 20,
            position_y6,
            pokemon_resistance_value,
            fontsize=20,
            color="black",
        )  # resistance value
    if prediction["data"].get("retreatCost"):
        plt.text(
            position_x6 - 10,
            position_y6,
            pokemon_retreat_cost,
            fontsize=8,
            color="black",
        )  # retreat cost
    plt.text(
        position_x1 + 10,
        position_y7,
        "Illus. LeWagon",
        fontsize=10,
        color="black",
        style="italic",
    )  # illustrator
    if prediction["data"].get("flavorText"):
        plt.text(
            position_x4,
            position_y7 + 15,
            pokemon_flavor_text,
            wrap=True,
            fontsize=10,
            color="black",
        )  # flavor text

        pokemon_flavorText = prediction["data"]["flavorText"]
    plt.savefig(
        "pokemon_card_generator/frontend/images/cache/cache_image.png"
    )  # save image
    init_image = Image.open(
        "pokemon_card_generator/frontend/images/cache/cache_image.png"
    )  # init image
    st.image(init_image, width=734)  # show image in streamlit


show_image()
