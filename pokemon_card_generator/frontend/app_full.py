import streamlit as st
import base64
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
response = requests.get(api, params=params)
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
# define paths
main_path = "pokemon_card_generator/frontend/images/"
set_path = main_path + "cleaned_cards"
ability_img_path = main_path + "card_icons/ability.png"
image_full_path = os.path.join(set_path, pokemon_type + ".png")
position_y4 = position_y3 + 60
position_y5 = position_y4 + 60
position_y6 = position_y5 + 60
position_y7 = position_y6 + 71
position_y8 = position_y7 + 30


# show image
background_image = open(image_full_path, "rb")
card_url = base64.b64encode(background_image.read()).decode("utf-8")
background_image.close()
# show image 2
ability_image = open(ability_img_path, "rb")
ability_url = base64.b64encode(ability_image.read()).decode("utf-8")
ability_image.close()

st.markdown(
    f'<img src="data:image/png;base64,{card_url}" alt="card background"><img src="data:image/png;base64,{ability_url}" alt="card background">',
    unsafe_allow_html=True,
)
