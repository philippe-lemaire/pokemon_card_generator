import streamlit as st
import requests
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import json
from pokemon_card_generator.data.pokemon_list import pokemon_list

st.markdown(
    "<h1 style='text-align: center; color: blue;'>Pokémon Card Generator</h1>",
    unsafe_allow_html=True,
)

# inputs
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

st.write(
    "<style>div.row-widget.stRadio > div{flex-direction:row;}</style>",
    unsafe_allow_html=True,
)

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

params = dict(name=pokemon_selected, rarity=rarity_selected)

response = requests.get(url, params=params)

prediction = response.json()

pokemon_type = prediction["data"]["types"][0].lower()
pokemon_name = prediction["data"]["name"]
hp = prediction["data"]["hp"]
nationalPokedexNumbers = prediction["data"]["nationalPokedexNumbers"][0]

if prediction["data"].get("abilities"):
    ability_name = prediction["data"]["abilities"][0]["name"]
    ability_text = prediction["data"]["abilities"][0]["text"]

# first text
first_position = 575
second_position = 625
third_position = 675
fourth_position = 725

# paths
set_path = "pokemon_card_generator/frontend/images/cleaned_cards"
image_full_path = os.path.join(set_path, pokemon_type + ".png")


def show_image():
    fig = plt.figure(frameon=True, figsize=(9, 12), dpi=100.0)
    plt.axis("on")

    ax1 = plt.imshow(mpimg.imread(image_full_path), alpha=0.7)
    plt.text(130, 72, pokemon_name, fontsize=25, color="black")
    plt.text(530, 72, "HP", fontsize=13, color="black")
    plt.text(560, 72, hp, fontsize=25, color="black")
    plt.text(
        367,
        506,
        "NO. " + str(nationalPokedexNumbers) + " Pokémon",
        ha="center",
        fontsize=12,
        color="black",
    )
    if prediction["data"].get("abilities"):
        plt.text(200, first_position, ability_name, fontsize=22, color="black")
        plt.text(
            50,
            second_position,
            ability_text,
            ha="left",
            fontsize=16,
            color="black",
            wrap=True,
            transform=plt.transAxes,
        )
    plt.savefig("pokemon_card_generator/frontend/images/cache/cache_image.png")
    init_image = Image.open(
        "pokemon_card_generator/frontend/images/cache/cache_image.png"
    )
    st.image(init_image, width=734)


show_image()
