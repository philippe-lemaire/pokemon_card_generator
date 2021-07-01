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
    pokemon_name = st.selectbox("", (pokemon_list))
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
url = "https://api.pokemontcg.io/v2/cards/xy7-19"

params = dict(name=pokemon_name, rarity=rarity_selected)

response = requests.get(url, params=params)

prediction = response.json()

pokemon_type = prediction["data"]["types"][0].lower()

# paths
set_path = "pokemon_card_generator/frontend/images/cleaned_cards"
image_full_path = os.path.join(set_path, pokemon_type + ".png")


def show_image():
    fig = plt.figure(frameon=True, figsize=(9, 12), dpi=100.0)
    plt.axis("off")

    ax1 = plt.imshow(mpimg.imread(image_full_path), alpha=0.7)
    plt.text(130, 70, pokemon_name, fontsize=15, color="black")
    plt.savefig("pokemon_card_generator/frontend/images/cache/cache_image.png")
    init_image = Image.open(
        "pokemon_card_generator/frontend/images/cache/cache_image.png"
    )
    st.image(init_image, width=734)


show_image()
